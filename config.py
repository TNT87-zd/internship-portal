import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "doi-key-nay-khi-deploy-that")

    # Mac dinh dung SQLite de chay/test ngay khong can cai MySQL.
    # Khi co MySQL, dat bien moi truong DATABASE_URL, vi du:
    #   mysql+pymysql://root:matkhau@localhost:3306/internship_portal
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'internship.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 6 * 1024 * 1024  # 6MB, du cho CV PDF <=5MB
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
