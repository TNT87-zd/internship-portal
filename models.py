from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SinhVien(db.Model):
    """Actor chinh cua UC-03."""
    __tablename__ = "sinh_vien"

    id = db.Column(db.Integer, primary_key=True)
    mssv = db.Column(db.String(20), unique=True, nullable=False)
    ho_ten = db.Column(db.String(120), nullable=False)
    lop = db.Column(db.String(30))
    truong = db.Column(db.String(120), default="Đại Học Duy Tân")
    email = db.Column(db.String(120))
    sdt = db.Column(db.String(15))

    don_dang_ky = db.relationship("DonDangKy", backref="sinh_vien", lazy=True)

    def __repr__(self):
        return f"<SinhVien {self.mssv} - {self.ho_ten}>"


class ViTriThucTap(db.Model):
    """Vi tri thuc tap dang mo - hien thi o UC-03."""
    __tablename__ = "vi_tri_thuc_tap"

    id = db.Column(db.Integer, primary_key=True)
    ten_vi_tri = db.Column(db.String(150), nullable=False)
    cong_ty = db.Column(db.String(150), nullable=False)
    dia_diem = db.Column(db.String(120))
    thoi_luong_tuan = db.Column(db.Integer, default=10)
    so_cho_con = db.Column(db.Integer, default=0)

    don_dang_ky = db.relationship("DonDangKy", backref="vi_tri", lazy=True)

    def __repr__(self):
        return f"<ViTri {self.ten_vi_tri} @ {self.cong_ty}>"


class DonDangKy(db.Model):
    """
    Don dang ky thuc tap.
    UC-03 tao ban ghi nay (trang_thai = cho_duyet).
    UC-04 cap nhat trang_thai (da_duyet / tu_choi).
    """
    __tablename__ = "don_dang_ky"

    id = db.Column(db.Integer, primary_key=True)
    sinh_vien_id = db.Column(db.Integer, db.ForeignKey("sinh_vien.id"), nullable=False)
    vi_tri_id = db.Column(db.Integer, db.ForeignKey("vi_tri_thuc_tap.id"), nullable=False)

    ngay_bat_dau = db.Column(db.Date, nullable=False)
    thoi_gian_tuan = db.Column(db.Integer, default=10)
    cv_filename = db.Column(db.String(255))
    ghi_chu = db.Column(db.Text)

    # cho_duyet | da_duyet | tu_choi | nhap
    trang_thai = db.Column(db.String(20), default="cho_duyet", nullable=False)
    ly_do_tu_choi = db.Column(db.Text)

    ngay_gui = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_xu_ly = db.Column(db.DateTime)

    def __repr__(self):
        return f"<DonDangKy #{self.id} - {self.trang_thai}>"
