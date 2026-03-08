import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_HOST     = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_USER     = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB       = os.getenv("MYSQL_DB", "ovasan")
    MYSQL_CURSORCLASS = "DictCursor"
    SECRET_KEY = os.getenv("SECRET_KEY")

    MAIL_SERVER   = "smtp.gmail.com"
    MAIL_PORT     = 465
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS  = False
    MAIL_USE_SSL  = True

    RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY", "6LfkEwYsAAAAAM5XI17sM2N9cxUzPKIdEu4lIl-7")
    MAIL_RECIPIENTS    = os.getenv("MAIL_RECIPIENTS", "burhankaratas771@gmail.com")