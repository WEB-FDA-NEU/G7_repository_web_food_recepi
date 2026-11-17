import os
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import LoginSession, User
from ..schemas import AccountUpdate, LoginIn, RegisterIn, UserOut
from ..security import (
    create_session_token,
    hash_password,
    hash_session_token,
    verify_password,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])
COOKIE_NAME = "login_session"
SESSION_MINUTES = int(os.getenv("SESSION_EXPIRE_MINUTES", "60"))


def _start_session(user: User, db: Session, response: Response) -> User:
    token = create_session_token()
    expires_at = datetime.now(UTC) + timedelta(minutes=SESSION_MINUTES)
    db.add(
        LoginSession(
            user_id=user.id,
            cookie_token_hash=hash_session_token(token),
            expires_at=expires_at,
        )
    )
    db.commit()
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        max_age=SESSION_MINUTES * 60,
        httponly=True,
        secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        samesite="lax",
        path="/",
    )
    return user


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterIn,
    response: Response,
    db: Session = Depends(get_db),
):
    exists = db.scalar(select(User).where(User.email == payload.email))
    if exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "This email is already in use.")
    username_exists = db.scalar(
        select(User).where(User.username == payload.username)
    )
    if username_exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "This username is already in use.")

    user = User(
        email=payload.email,
        username=payload.username,
        password_hash=hash_password(payload.password),
        display_name=payload.display_name,
        phone=payload.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _start_session(user, db, response)


@router.post("/login", response_model=UserOut)
def login(payload: LoginIn, response: Response, db: Session = Depends(get_db)):
    user = db.scalar(
        select(User).where(
            (User.email == payload.identifier)
            | (User.username == payload.identifier)
        )
    )
    # Cố tình trả lỗi giống nhau cho "sai email" và "sai mật khẩu" để không lộ
    # cho người ngoài biết một email cụ thể có tồn tại trong hệ thống hay không.
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "The email or password doesn't match.",
        )
    return _start_session(user, db, response)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    token = request.cookies.get(COOKIE_NAME)
    if token:
        login_session = db.scalar(
            select(LoginSession).where(
                LoginSession.cookie_token_hash == hash_session_token(token),
                LoginSession.revoked_at.is_(None),
            )
        )
        if login_session:
            login_session.revoked_at = datetime.now(UTC)
            db.commit()
    response.delete_cookie(COOKIE_NAME, path="/")
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


@router.patch("/me", response_model=UserOut)
def update_me(
    payload: AccountUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.display_name is None and payload.new_password is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Enter a new name or password.")
    if payload.display_name is not None:
        if not payload.display_name:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Enter your name.")
        user.display_name = payload.display_name
    if payload.new_password is not None:
        if not payload.current_password:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Enter your current password.")
        if not verify_password(payload.current_password, user.password_hash):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Your current password is incorrect.")
        user.password_hash = hash_password(payload.new_password)
    db.commit()
    db.refresh(user)
    return user
