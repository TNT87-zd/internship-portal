import os
from datetime import datetime, date

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, abort
)
from werkzeug.utils import secure_filename

from config import Config
from models import db, SinhVien, ViTriThucTap, DonDangKy

ALLOWED_EXT = {"pdf"}


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        _seed_du_lieu_mau()

    register_routes(app)
    return app


def _seed_du_lieu_mau():
    """Tao du lieu mau lan dau chay, de demo UC-03/UC-04 ngay khong can nhap tay."""
    if SinhVien.query.first():
        return  # da co du lieu roi, khong seed lai

    sv = SinhVien(
        mssv="29211164915", ho_ten="Trương Nhật Trường",
        lop="CS434M", truong="Đại Học Duy Tân",
        email="sv@duytan.edu.vn", sdt="0905123456",
    )
    sv2 = SinhVien(
        mssv="21IT02", ho_ten="Mai Văn Chung",
        lop="21IT02", truong="Đại Học Duy Tân",
        email="chung.mv@duytan.edu.vn", sdt="0905123457",
    )
    db.session.add_all([sv, sv2])

    vt1 = ViTriThucTap(
        ten_vi_tri="Thực tập sinh Marketing", cong_ty="FPT Telecom",
        dia_diem="Đà Nẵng", thoi_luong_tuan=10, so_cho_con=3,
    )
    vt2 = ViTriThucTap(
        ten_vi_tri="Thực tập sinh Dev ReactJS", cong_ty="Viettel Solutions",
        dia_diem="Hà Nội / Đà Nẵng", thoi_luong_tuan=12, so_cho_con=1,
    )
    vt3 = ViTriThucTap(
        ten_vi_tri="Frontend Developer", cong_ty="VNG Corporation",
        dia_diem="TP.HCM", thoi_luong_tuan=8, so_cho_con=2,
    )
    db.session.add_all([vt1, vt2, vt3])
    db.session.commit()

    don = DonDangKy(
        sinh_vien_id=sv.id, vi_tri_id=vt1.id,
        ngay_bat_dau=date(2026, 11, 1), thoi_gian_tuan=10,
        cv_filename="CV_TruongNhatTruong.pdf",
        ghi_chu="Mong muốn thực tập mảng backend.",
        trang_thai="cho_duyet",
    )
    db.session.add(don)
    db.session.commit()


def register_routes(app):

    # ---------- Trang chu ----------
    @app.route("/")
    def trang_chu():
        return redirect(url_for("uc03_dang_ky"))

    # =========================================================
    #  UC-03 : DANG KY VI TRI THUC TAP  (actor: Sinh vien)
    # =========================================================
    @app.route("/dang-ky", methods=["GET"])
    def uc03_dang_ky():
        # actor "dang nhap" - o day demo co dinh 1 sinh vien dau tien
        sinh_vien = SinhVien.query.first()

        # dieu kien truoc: khong duoc co qua 1 don cho_duyet
        don_cho_duyet = DonDangKy.query.filter_by(
            sinh_vien_id=sinh_vien.id, trang_thai="cho_duyet"
        ).first()

        vi_tri_list = ViTriThucTap.query.filter(ViTriThucTap.so_cho_con > 0).all()

        return render_template(
            "uc03_dangky.html",
            sinh_vien=sinh_vien,
            vi_tri_list=vi_tri_list,
            don_cho_duyet=don_cho_duyet,
            today=date.today().isoformat(),
        )

    @app.route("/dang-ky", methods=["POST"])
    def uc03_dang_ky_submit():
        sinh_vien = SinhVien.query.first()

        # --- quy tac nghiep vu: chan neu da co don cho_duyet ---
        don_cho_duyet = DonDangKy.query.filter_by(
            sinh_vien_id=sinh_vien.id, trang_thai="cho_duyet"
        ).first()
        if don_cho_duyet:
            flash("Bạn đang có 1 đơn ở trạng thái Chờ duyệt, không thể gửi thêm.", "error")
            return redirect(url_for("uc03_dang_ky"))

        vi_tri_id = request.form.get("vi_tri_id", type=int)
        vi_tri = ViTriThucTap.query.get_or_404(vi_tri_id)

        if vi_tri.so_cho_con <= 0:
            flash("Vị trí này đã hết chỗ trống.", "error")
            return redirect(url_for("uc03_dang_ky"))

        ngay_bat_dau_raw = request.form.get("ngay_bat_dau")
        thoi_gian_tuan = request.form.get("thoi_gian_tuan", type=int, default=10)
        ghi_chu = request.form.get("ghi_chu", "")
        cam_ket = request.form.get("cam_ket")

        if not ngay_bat_dau_raw or not cam_ket:
            flash("Vui lòng nhập đủ thông tin bắt buộc và tick cam kết.", "error")
            return redirect(url_for("uc03_dang_ky"))

        # --- luong con «include»: tai len CV ---
        cv_file = request.files.get("cv_file")
        cv_filename = None
        if cv_file and cv_file.filename:
            ext = cv_file.filename.rsplit(".", 1)[-1].lower()
            if ext not in ALLOWED_EXT:
                flash("CV phải ở định dạng PDF.", "error")
                return redirect(url_for("uc03_dang_ky"))
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            cv_filename = secure_filename(f"{sinh_vien.mssv}_{cv_file.filename}")
            cv_file.save(os.path.join(Config.UPLOAD_FOLDER, cv_filename))
        else:
            flash("Vui lòng đính kèm CV (PDF).", "error")
            return redirect(url_for("uc03_dang_ky"))

        don = DonDangKy(
            sinh_vien_id=sinh_vien.id,
            vi_tri_id=vi_tri.id,
            ngay_bat_dau=datetime.strptime(ngay_bat_dau_raw, "%Y-%m-%d").date(),
            thoi_gian_tuan=thoi_gian_tuan,
            cv_filename=cv_filename,
            ghi_chu=ghi_chu,
            trang_thai="cho_duyet",
        )
        db.session.add(don)
        db.session.commit()

        flash("Gửi đăng ký thành công! Đơn của bạn đang chờ duyệt.", "success")
        return redirect(url_for("uc03_dang_ky"))

    # =========================================================
    #  UC-04 : XET DUYET DANG KY THUC TAP  (actor: Chuyen vien Dao tao)
    # =========================================================
    @app.route("/phe-duyet")
    def uc04_phe_duyet():
        tab = request.args.get("tab", "cho_duyet")
        selected_id = request.args.get("chon", type=int)

        query = DonDangKy.query
        if tab != "tat_ca":
            query = query.filter_by(trang_thai=tab)
        don_list = query.order_by(DonDangKy.ngay_gui.desc()).all()

        stats = {
            "tong": DonDangKy.query.count(),
            "cho_duyet": DonDangKy.query.filter_by(trang_thai="cho_duyet").count(),
            "da_duyet": DonDangKy.query.filter_by(trang_thai="da_duyet").count(),
            "tu_choi": DonDangKy.query.filter_by(trang_thai="tu_choi").count(),
        }

        don_chon = None
        if selected_id:
            don_chon = DonDangKy.query.get(selected_id)
        elif don_list:
            don_chon = don_list[0]

        return render_template(
            "uc04_pheduyet.html",
            don_list=don_list, stats=stats, tab=tab, don_chon=don_chon,
        )

    @app.route("/phe-duyet/<int:don_id>/duyet", methods=["POST"])
    def uc04_duyet_don(don_id):
        don = DonDangKy.query.get_or_404(don_id)
        if don.trang_thai != "cho_duyet":
            flash("Đơn này đã được xử lý trước đó.", "error")
            return redirect(url_for("uc04_phe_duyet"))

        # --- quy tac nghiep vu: duyet -> tru cho trong + cap nhat trang thai ---
        don.trang_thai = "da_duyet"
        don.ngay_xu_ly = datetime.utcnow()
        if don.vi_tri.so_cho_con > 0:
            don.vi_tri.so_cho_con -= 1
        db.session.commit()

        flash(f"Đã duyệt đơn của {don.sinh_vien.ho_ten}.", "success")
        return redirect(url_for("uc04_phe_duyet", tab="cho_duyet"))

    @app.route("/phe-duyet/<int:don_id>/tu-choi", methods=["POST"])
    def uc04_tu_choi_don(don_id):
        don = DonDangKy.query.get_or_404(don_id)
        if don.trang_thai != "cho_duyet":
            flash("Đơn này đã được xử lý trước đó.", "error")
            return redirect(url_for("uc04_phe_duyet"))

        ly_do = request.form.get("ly_do", "").strip()
        if not ly_do:
            flash("Bắt buộc nhập lý do khi từ chối.", "error")
            return redirect(url_for("uc04_phe_duyet", chon=don_id))

        # --- quy tac nghiep vu: tu choi -> luu ly do ---
        don.trang_thai = "tu_choi"
        don.ly_do_tu_choi = ly_do
        don.ngay_xu_ly = datetime.utcnow()
        db.session.commit()

        flash(f"Đã từ chối đơn của {don.sinh_vien.ho_ten}.", "success")
        return redirect(url_for("uc04_phe_duyet", tab="cho_duyet"))


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
