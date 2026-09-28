-- Schema MySQL cho He thong Quan ly Thuc tap
-- Chay: mysql -u root -p < schema.sql
-- (hoac khong can chay tay - app.py da tu tao bang bang SQLAlchemy khi khoi dong)

CREATE DATABASE IF NOT EXISTS internship_portal
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE internship_portal;

CREATE TABLE IF NOT EXISTS sinh_vien (
  id INT AUTO_INCREMENT PRIMARY KEY,
  mssv VARCHAR(20) NOT NULL UNIQUE,
  ho_ten VARCHAR(120) NOT NULL,
  lop VARCHAR(30),
  truong VARCHAR(120) DEFAULT 'Đại Học Duy Tân',
  email VARCHAR(120),
  sdt VARCHAR(15)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS vi_tri_thuc_tap (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ten_vi_tri VARCHAR(150) NOT NULL,
  cong_ty VARCHAR(150) NOT NULL,
  dia_diem VARCHAR(120),
  thoi_luong_tuan INT DEFAULT 10,
  so_cho_con INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS don_dang_ky (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sinh_vien_id INT NOT NULL,
  vi_tri_id INT NOT NULL,
  ngay_bat_dau DATE NOT NULL,
  thoi_gian_tuan INT DEFAULT 10,
  cv_filename VARCHAR(255),
  ghi_chu TEXT,
  trang_thai VARCHAR(20) NOT NULL DEFAULT 'cho_duyet',  -- cho_duyet | da_duyet | tu_choi
  ly_do_tu_choi TEXT,
  ngay_gui DATETIME DEFAULT CURRENT_TIMESTAMP,
  ngay_xu_ly DATETIME,
  FOREIGN KEY (sinh_vien_id) REFERENCES sinh_vien(id),
  FOREIGN KEY (vi_tri_id) REFERENCES vi_tri_thuc_tap(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Du lieu mau (tuong tu seed trong app.py)
INSERT INTO sinh_vien (mssv, ho_ten, lop, truong, email, sdt) VALUES
  ('29211164915', 'Trương Nhật Trường', 'CS434M', 'Đại Học Duy Tân', 'sv@duytan.edu.vn', '0905123456');

INSERT INTO vi_tri_thuc_tap (ten_vi_tri, cong_ty, dia_diem, thoi_luong_tuan, so_cho_con) VALUES
  ('Thực tập sinh Marketing', 'FPT Telecom', 'Đà Nẵng', 10, 3),
  ('Thực tập sinh Dev ReactJS', 'Viettel Solutions', 'Hà Nội / Đà Nẵng', 12, 1),
  ('Frontend Developer', 'VNG Corporation', 'TP.HCM', 8, 2);
