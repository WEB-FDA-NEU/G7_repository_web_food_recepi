import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DEFAULT_DATABASE = Path(__file__).resolve().parent.parent / "database" / "data.sqlite3"
DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{DEFAULT_DATABASE}"

# Vercel's function filesystem is ephemeral. Require an external database there
# so a missing project setting cannot silently create a disposable SQLite DB.
if os.getenv("VERCEL") and not os.getenv("DATABASE_URL"):
    raise RuntimeError("Set DATABASE_URL to a persistent database in Vercel.")

# Neon/Heroku đưa chuỗi bắt đầu bằng "postgres://", SQLAlchemy 2.x cần "postgresql://".
# Thiếu 3 dòng này là deploy hỏng, và lỗi báo rất khó hiểu.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
