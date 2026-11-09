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

### Xem giao diện (frontend, Milestone 1 — chỉ HTML)

```bash
uv run python -m http.server 5500 --directory frontend
```

### Chạy backend (từ các milestone có API)

** macOS / Linux/ Windows**:
see [mise.tom](mise.toml)

