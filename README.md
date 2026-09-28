# Hệ thống Quản lý Thực tập — UC-03 & UC-04

Đồ án môn **Công cụ & Phương pháp Quản lý Thiết kế Hệ thống**.
Triển khai 2 use case được phân công: **UC-03 — Đăng ký vị trí thực tập** (Sinh viên) và **UC-04 — Phê duyệt đăng ký thực tập** (Chuyên viên Đào tạo).

Stack: **Python (Flask) + SQLAlchemy + MySQL** (mặc định dùng SQLite để chạy/test ngay không cần cài MySQL).

## Cấu trúc thư mục

```
internship-portal/
├── app.py              # Route xử lý UC-03 & UC-04
├── models.py            # Model: SinhVien, ViTriThucTap, DonDangKy
├── config.py             # Cấu hình DB (SQLite mặc định / MySQL qua .env)
├── schema.sql            # Schema MySQL (dùng khi deploy MySQL thật)
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── uc03_dangky.html      # Giao diện UC-03
│   └── uc04_pheduyet.html    # Giao diện UC-04
└── static/
    ├── css/style.css
    └── uploads/               # Nơi lưu CV sinh viên tải lên
```

## Cách chạy (local, dùng SQLite — nhanh nhất để demo)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Mở trình duyệt: `http://127.0.0.1:5000` → tự chuyển đến UC-03.
Lần chạy đầu tiên, app tự tạo bảng và chèn sẵn 1 sinh viên + 3 vị trí thực tập mẫu để demo ngay.

## Chuyển sang MySQL (khi cần dùng DB thật)

1. Cài MySQL, tạo database bằng `schema.sql`:
   ```bash
   mysql -u root -p < schema.sql
   ```
2. Copy `.env.example` thành `.env`, sửa `DATABASE_URL` cho đúng user/mật khẩu MySQL của bạn.
3. Cài thêm biến môi trường trước khi chạy (hoặc dùng `python-dotenv` nếu muốn tự động load `.env`):
   ```bash
   export DATABASE_URL="mysql+pymysql://root:matkhau@localhost:3306/internship_portal"
   python app.py
   ```

## Ánh xạ route ↔ Use Case

| Route | Method | Use Case | Mô tả |
|---|---|---|---|
| `/dang-ky` | GET | UC-03 | Hiển thị form đăng ký + danh sách vị trí đang mở |
| `/dang-ky` | POST | UC-03 | Xử lý gửi đăng ký (kiểm tra 1-đơn-chờ-duyệt, upload CV) |
| `/phe-duyet` | GET | UC-04 | Danh sách hồ sơ + thống kê + panel chi tiết |
| `/phe-duyet/<id>/duyet` | POST | UC-04 | Duyệt đơn — trừ chỗ trống vị trí |
| `/phe-duyet/<id>/tu-choi` | POST | UC-04 | Từ chối đơn — bắt buộc nhập lý do |

Các quy tắc nghiệp vụ trong đặc tả use case (1 đơn chờ duyệt/sinh viên, bắt buộc lý do khi từ chối, trừ chỗ trống khi duyệt...) đã được cài đặt và kiểm thử trong `app.py`.

## Đẩy lên GitHub

```bash
cd internship-portal
git init
git add .
git commit -m "Init: UC-03 dang ky va UC-04 phe duyet thuc tap"
git branch -M main
git remote add origin https://github.com/<username>/<ten-repo>.git
git push -u origin main
```

> Lưu ý: file `.env`, `*.db` (SQLite) và `static/uploads/*` (CV thật của sinh viên) đã được loại trừ qua `.gitignore` — không đẩy dữ liệu nhạy cảm lên GitHub.
