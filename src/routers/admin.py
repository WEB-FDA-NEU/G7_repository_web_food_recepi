from fastapi import APIRouter, Depends
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database import engine, get_db
from ..deps import get_admin
from ..models import User
from ..schemas import AdminUserOut

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats")
def get_stats(
    _: User = Depends(get_admin),
    db: Session = Depends(get_db),
):
    """Return admin dashboard counts and the current SQLite file size."""
    user_count = db.scalar(select(func.count()).select_from(User)) or 0
    database_size_bytes = None
    if engine.dialect.name == "sqlite":
        database_path = engine.url.database
        if database_path and database_path != ":memory:":
            try:
                database_size_bytes = Path(database_path).stat().st_size
            except OSError:
                pass
    return {
        "user_count": user_count,
        "database_size_bytes": database_size_bytes,
    }


@router.get("/users", response_model=list[AdminUserOut])
def list_users(
    _: User = Depends(get_admin),
    db: Session = Depends(get_db),
):
    return db.scalars(select(User).order_by(User.created_at.desc())).all()
