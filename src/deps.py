from datetime import UTC, datetime

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db
from .models import LoginSession, User
from .security import hash_session_token


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    """Authenticate a request using its HttpOnly login-session cookie."""
    token = request.cookies.get("login_session")
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Please sign in to continue.")
    login_session = db.scalar(
        select(LoginSession).where(
            LoginSession.cookie_token_hash == hash_session_token(token),
            LoginSession.revoked_at.is_(None),
            LoginSession.expires_at > datetime.now(UTC),
        )
    )
    user = db.get(User, login_session.user_id) if login_session else None
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Please sign in again to continue.")
    return user


def get_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You don't have permission to open this page.")
    return user
