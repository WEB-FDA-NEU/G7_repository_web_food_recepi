import os
from uuid import uuid4
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .deps import get_current_user
from .models import User
from .routers import admin, auth, recipes


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Schema creation is idempotent and centralized in database/note.py.
    from database.note import initialize_schema

    initialize_schema()
    yield


app = FastAPI(
    title="Ladle API",
    version="1.0.0",
    description="API cho nền tảng chia sẻ công thức nấu ăn Ladle. Tài liệu tự sinh tại /docs.",
    lifespan=lifespan,
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
app.include_router(admin.router)


@app.get("/api/health", tags=["ops"])
def health():
    return {"status": "ok"}


FRONTEND = Path(__file__).resolve().parent.parent / "frontend"


@app.get("/admin_console", include_in_schema=False)
def admin_console():
    return FileResponse(FRONTEND / "admin_console.html")


@app.get("/userhome", include_in_schema=False)
def user_home():
    return FileResponse(FRONTEND / "userhome.html")


# ---- Serve frontend (Mốc 4) --------------------------------------------
# Đặt CUỐI CÙNG, sau tất cả router API. Nếu mount ở trên thì "/" nuốt hết
# và mọi request /api/... sẽ ra 404.
UPLOADS = (
    Path("/tmp/ladle-uploads")
    if os.getenv("VERCEL")
    else Path(__file__).resolve().parent / "uploads"
)
UPLOADS.mkdir(exist_ok=True)


@app.post("/api/uploads/recipe-image", status_code=status.HTTP_201_CREATED)
async def upload_recipe_image(
    image: UploadFile = File(...),
    _: User = Depends(get_current_user),
):
    """Store a small JPEG, PNG, or WebP recipe image and return its public URL."""
    content = await image.read(5 * 1024 * 1024 + 1)
    await image.close()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status.HTTP_413_CONTENT_TOO_LARGE, "Images must be 5 MB or smaller.")

    signatures = (
        (content.startswith(b"\xff\xd8\xff"), "jpg"),
        (content.startswith(b"\x89PNG\r\n\x1a\n"), "png"),
        (content.startswith(b"RIFF") and content[8:12] == b"WEBP", "webp"),
    )
    extension = next((ext for valid, ext in signatures if valid), None)
    if extension is None:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "Upload a JPEG, PNG, or WebP image.",
        )

    filename = f"{uuid4().hex}.{extension}"
    (UPLOADS / filename).write_bytes(content)
    return {"cover_url": f"/uploads/{filename}"}


app.mount("/uploads", StaticFiles(directory=UPLOADS), name="uploads")

if FRONTEND.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="frontend")
