# Ovasan Website

Ovasan Mühendislik web sitesi için Flask tabanlı bir uygulama. Ana sayfa, hakkımızda, hizmetler, projeler ve iletişim formu; ayrıca yönetim paneli ile içerik yönetimini destekler.

**Öne çıkanlar**
- Flask Blueprint yapısı (main, auth, admin)
- MySQL veritabanı entegrasyonu
- İletişim formu + e-posta gönderimi (Flask-Mail)
- reCAPTCHA doğrulaması

## Gereksinimler
- Python 3.10+ (önerilen)
- MySQL 5.7+ / 8+

## Kurulum
1. Sanal ortam oluşturun ve aktif edin
```bash
python -m venv venv
source venv/bin/activate
```

2. Bağımlılıkları kurun
```bash
pip install -r requirements.txt
```

3. Veritabanı oluşturun
```sql
CREATE DATABASE ovasan;
```

4. Ortam değişkenlerini ayarlayın (`.env` dosyası oluşturun)
```ini
SECRET_KEY=your_secret_key

PANEL_USERNAME=admin
PANEL_PASSWORD=strong_password

MAIL_USERNAME=your_gmail_address
MAIL_PASSWORD=your_gmail_app_password

CAPTCHA_SECRET_KEY=your_recaptcha_secret_key
```

Notlar:
- Gmail kullanıyorsanız uygulama şifresi gerekir.
- reCAPTCHA anahtarları Google reCAPTCHA panelinden alınır.

## Çalıştırma
```bash
python run.py
```
Uygulama varsayılan olarak `http://localhost:5000` üzerinde çalışır.

## Dizin Yapısı
- `app/controllers` route ve iş mantığı
- `app/models` veritabanı işlemleri
- `app/templates` HTML şablonları
- `app/utils` yardımcı fonksiyonlar (auth, mail vb.)
- `app/extensions.py` üçüncü parti eklentiler (MySQL, Mail)

## Yönetim Paneli
`/login` üzerinden giriş yapılır. Kimlik bilgileri `.env` içindeki `PANEL_USERNAME` ve `PANEL_PASSWORD` ile kontrol edilir.

## İletişim Formu
`/contact` sayfasındaki form gönderimleri:
- reCAPTCHA doğrulamasından geçer
- Mail ile belirtilen alıcıya iletilir
- Dosya eklerini ve boyut sınırlamasını kontrol eder

## Geliştirme Notları
- MySQL ayarları `config.py` içinde yapılandırılır.
- Mail ayarları `config.py` + `.env` üzerinden yönetilir.

---

Herhangi bir geliştirme önerin varsa memnuniyetle yardımcı olurum.
