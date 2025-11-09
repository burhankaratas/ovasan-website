from flask import session, flash, redirect, url_for
from dotenv import load_dotenv
from functools import wraps
import requests
import os

def verify_recaptcha(response_token: str):
    """Google reCAPTCHA doğrulaması yapar. 
    Başarılıysa (True, None) döner; başarısızsa (False, hata_mesajı)."""

    load_dotenv()    
    secret_key = os.getenv("CAPTCHA_SECRET_KEY")
    if not secret_key:
        raise RuntimeError("Sunucu yapılandırmasında reCAPTCHA gizli anahtarı bulunamadı.")
    
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": secret_key,
        "response": response_token
    }

    try:
        r = requests.post(url, data=data)
        result = r.json()
    except Exception as e:
        return False, f"Doğrulama isteği başarısız: {e}"

    if result.get("success"):
        return True, None
    else:
        # Google döndürdüğü hata kodlarını liste halinde verir.
        error_codes = result.get("error-codes", [])
        return False, f"reCAPTCHA doğrulaması başarısız: {error_codes}"

def user_authentication(username, password):
    """
    username, password değişkenlerini alır ve .env deki değerler ile kıyaslar.
    Yanlış veya eksik ise False, "Hata Mesajı"
    Doğru ise True, None 
    """

    load_dotenv()

    real_username = os.getenv("PANEL_USERNAME")
    real_password = os.getenv("PANEL_PASSWORD")

    if real_username != username or real_password != password:
        return False, "Eksik veya yanlış giriş bilgileri girdiniz. Bilgilerinizi kontrol edip tekrar deneyiniz."
    
    return True, "Başarılı giriş"

def login_required(f):
    """
    Bu decorator, kullanıcı giriş yapmamışsa login sayfasına yönlendirir.
    session['logged_in'] yoksa veya False ise çalışır.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Bu sayfayı görüntülemek için giriş yapmalısınız.", "warning")
            return redirect(url_for("auth.login")) 
        return f(*args, **kwargs)
    return decorated_function