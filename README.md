# web_design_and_program
Nền tảng chia sẻ công thức nấu ăn — một website cho phép người dùng đăng tải, tìm kiếm và đánh giá công thức nấu ăn blablabla.
## Thành viên

| name           | github         | role   |
| -------------- | -------------- | ------ |
| bế Thành Đạt   | th3dummyking   | leader0 |
| Phan Hải Đăng  | phandang2310   | member |
| minhquang      | iambadwithname | leader1  |
| Bùi Khang Long | longbk761-bot  | member |

## Mục tiêu
Nền tảng chia sẻ công thức nấu ăn là một website cho phép người dùng:

- đăng tải công thức
- đánh giá các công thức nấu ăn
- tìm kiếm công thức
- admin


## requirement

- **[uv](https://docs.astral.sh/uv/)** — trình quản lý gói và môi trường ảo cho Python, dùng để cài dependency và chạy dự án.
- **[mise](https://mise.jdx.dev/installing-mise.html)** —(optional) also an env/tool manager.
- **Git** — để tải mã nguồn về máy.

---

## 1. Cài đặt uv

- unix:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

* Windows:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---
## 2. Tải dự án về máy

** macOS / Linux/Windows**:

```
git clone https://github.com/<tên-tổ-chức-hoặc-user>/web_design_and_program.git
cd web_design_and_program
```
---
## 3. Cài đặt dependencies

uv sync
```
- Unix:
```bash
source .venv/bin/activate
```

- Windows:

```powershell
.venv\Scripts\Activate.ps1
```

## 4. Chạy dự án

### Chạy website có API (đăng nhập, admin)

```bash
uv run uvicorn src.main:app --reload --port 10000
```

Mở `http://127.0.0.1:10000`. FastAPI phục vụ cả frontend lẫn API trên cùng địa chỉ.

### Chạy frontend và backend riêng

Terminal 1:

```bash
uv run uvicorn src.main:app --reload --port 10000
```

Terminal 2:

```bash
uv run python -m http.server 5500 --directory frontend
```

Mở `http://127.0.0.1:5500`. Frontend sẽ gọi API tại cổng `10000`.

## Deploy on Vercel

The root `vercel.json` configures two Vercel services: static HTML/CSS/JS from
`frontend/`, and the FastAPI app at `src.main:app`. The frontend is public at `/`;
API requests under `/api/` are routed to FastAPI. `/admin_console` and `/userhome`
are rewritten to their matching static HTML files. `/docs`, `/redoc`, and
`/openapi.json` are routed to FastAPI. The frontend calls the API through same-origin
`/api` URLs, so no internal service binding is needed.

The Python runtime is pinned to 3.14 by `.python-version`. The FastAPI service uses
`pyproject.toml` and `uv.lock` for dependencies. Add these environment variables to
the Vercel project before deployment:

| Variable | Value |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection string from your database provider |
| `COOKIE_SECURE` | `true` |

On startup, the app creates any missing tables through `database/note.py`. This does
not migrate existing SQLite records or seed demo accounts; existing data must be
migrated separately, and users can register after the first deploy. In Vercel, select
the **Services** framework for the project and deploy from the repository root.
The health endpoint is `/api/health` and API docs are at `/docs`.
