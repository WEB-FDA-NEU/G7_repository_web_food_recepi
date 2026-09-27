# web_design_and_program

Nền tảng chia sẻ công thức nấu ăn — một website cho phép người dùng đăng tải, tìm kiếm và đánh giá công thức nấu ăn.

## Thành viên

| name           | github         | role   |
| -------------- | -------------- | ------ |
| bế Thành Đạt   | th3dummyking   | leader |
| Phan Hải Đăng  | phandang2310   | member |
| minhquang      | iambadwithname | member |
| Bùi Khang Long | longbk761-bot  | member |

## Mục tiêu

Nền tảng chia sẻ công thức nấu ăn là một website cho phép người dùng:

- đăng tải công thức
- tìm kiếm công thức
- và đánh giá các công thức nấu ăn

Người dùng có thể tạo công thức mới với danh sách nguyên liệu, các bước thực hiện, và hình ảnh minh họa; tìm kiếm công thức theo nguyên liệu có sẵn; lưu công thức yêu thích; và đánh giá, bình luận công thức của người khác.

> **Milestone 1**: chỉ dùng HTML, các trang được liên kết với nhau cũng bằng HTML thuần (chưa cần cài backend để xem giao diện).

---

## Yêu cầu hệ thống

- **Python 3.11 trở lên** — kiểm tra bằng `python --version` (macOS/Linux) hoặc `python --version` / `py --version` (Windows).
- **[uv](https://docs.astral.sh/uv/)** — trình quản lý gói và môi trường ảo cho Python, dùng để cài dependency và chạy dự án.
- **Git** — để tải mã nguồn về máy.

Nếu máy chưa có Python 3.11+, có thể để `uv` tự tải và quản lý Python giúp bạn (xem bước 3).

---

## 1. Cài đặt uv

** macOS / Linux** (Terminal):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

** Windows** (PowerShell):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Sau khi cài xong, mở lại terminal và kiểm tra:
```bash
uv --version
```

---

## 2. Tải dự án về máy

** macOS / Linux**:
```bash
git clone https://github.com/<tên-tổ-chức-hoặc-user>/web_design_and_program.git
cd web_design_and_program
```

** Windows** (PowerShell):
```powershell
git clone https://github.com/<tên-tổ-chức-hoặc-user>/web_design_and_program.git
cd web_design_and_program
```

> Không có Git? Vào trang GitHub của dự án → nút **Code** → **Download ZIP**, rồi giải nén ra và mở terminal tại thư mục đó.

---

## 3. Cài đặt dependencies

Chạy trong thư mục gốc của dự án (lệnh giống nhau trên cả hai hệ điều hành):

```bash
uv sync
```

Lệnh này sẽ:
- tự tải đúng phiên bản Python cần thiết nếu máy chưa có,
- tạo một môi trường ảo `.venv` riêng cho dự án,
- cài toàn bộ thư viện đúng phiên bản đã khai báo.

Không cần tự kích hoạt (activate) môi trường ảo — dùng `uv run ...` ở bước dưới, `uv` sẽ tự chạy trong đúng môi trường đó. Nếu muốn kích hoạt thủ công (ví dụ để trình biên tập code nhận đúng thư viện):

** macOS / Linux**:
```bash
source .venv/bin/activate
```

** Windows** (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

---

## 4. Chạy dự án

### Xem giao diện (frontend, Milestone 1 — chỉ HTML)

Cách đơn giản nhất: mở trực tiếp file `frontend/index.html` bằng trình duyệt.

Nếu muốn chạy qua một local server (khuyên dùng, để đường dẫn giữa các trang hoạt động đúng như khi deploy):

** macOS / Linux**:
```bash
uv run python -m http.server 5500 --directory frontend
```

** Windows** (PowerShell):
```powershell
uv run python -m http.server 5500 --directory frontend
```

Sau đó mở trình duyệt vào: **http://localhost:5500**

### Chạy backend (từ các milestone có API)

** macOS / Linux**:
```bash
uv run uvicorn main:app --reload
```

** Windows** (PowerShell):
```powershell
uv run uvicorn main:app --reload
```

Mặc định server chạy tại **http://127.0.0.1:8000** (chỉ máy này truy cập được). Tài liệu API tự sinh tại **http://127.0.0.1:8000/docs**.

Muốn cho máy khác trong cùng mạng Wi-Fi truy cập, thêm `--host 0.0.0.0`:

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

rồi vào bằng địa chỉ IP của máy chạy server, ví dụ `http://192.168.1.42:8000` (xem IP bằng `ipconfig` trên Windows hoặc `ifconfig`/`ipconfig getifaddr en0` trên macOS).

---

## Tóm tắt nhanh

| Bước              | macOS / Linux                                  | Windows (PowerShell)                           |
| ----------------- | ----------------------------------------------- | ----------------------------------------------- |
| Cài uv            | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| Tải dự án         | `git clone ...`                                 | `git clone ...`                                 |
| Cài dependencies  | `uv sync`                                       | `uv sync`                                       |
| Kích hoạt venv (tuỳ chọn) | `source .venv/bin/activate`             | `.venv\Scripts\Activate.ps1`                    |
| Chạy backend      | `uv run uvicorn main:app --reload`              | `uv run uvicorn main:app --reload`              |