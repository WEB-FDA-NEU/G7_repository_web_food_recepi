import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routers import auth, recipes

Base.metadata.create_all(engine)  # Mốc 3 dùng tạm. Dự án thật dùng Alembic migration.

app = FastAPI(
    title="Ladle API",
    version="1.0.0",
    description="API cho nền tảng chia sẻ công thức nấu ăn Ladle. Tài liệu tự sinh tại /docs.",
)

# CORS chỉ cần khi frontend chạy ở cổng khác (lúc phát triển: Live Server 5500).
# Khi deploy, FastAPI serve luôn frontend nên cùng origin, không cần CORS.
origins = os.getenv(
    "CORS_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500"
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(recipes.router)
app.include_router(recipes.me_router)
# TODO: thêm router của các thành viên khác ở đây (vd. bình luận, đánh giá sao)


@app.get("/api/health", tags=["ops"])
def health():
    return {"status": "ok"}


# ---- Serve frontend (Mốc 4) --------------------------------------------
# Đặt CUỐI CÙNG, sau tất cả router API. Nếu mount ở trên thì "/" nuốt hết
# và mọi request /api/... sẽ ra 404.
UPLOADS = Path(__file__).resolve().parent / "uploads"
UPLOADS.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOADS), name="uploads")

FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
print(FRONTEND)
if FRONTEND.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="frontend")
