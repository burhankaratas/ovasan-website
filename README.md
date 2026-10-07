# Ovasan Website

> Ovasan Mühendislik için geliştirilmiş kurumsal web sitesi ve içerik yönetim paneli.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)
![Lisans](https://img.shields.io/badge/license-MIT-green)

Kurumsal tanıtım sitesi: ana sayfa, hakkımızda, hizmetler, projeler ve iletişim.
İçerikler yönetim panelinden güncellenebilir; iletişim formu reCAPTCHA ile
doğrulanıp e-posta olarak iletilir.

## Özellikler

- **Kurumsal sayfalar** — ana sayfa, hakkımızda, hizmetler, projeler, kariyer, iletişim.
- **Hizmet & proje katalogları** — kategori listeleri ve detay sayfaları.
- **Yönetim paneli** — `/login` üzerinden giriş; içerik yönetimi.
- **İletişim formu** — reCAPTCHA doğrulaması + dosya eki ve boyut kontrolü.
- **E-posta gönderimi** — Flask-Mail ile SMTP üzerinden iletim.
- **Katmanlı mimari** — Flask Blueprint (main, auth, admin).

## Teknoloji Yığını

| Katman | Kullanılan |
|---|---|
| Backend | Python 3.12, Flask 3.1 |
| Veritabanı | MySQL, `flask-mysqldb` |
| E-posta | Flask-Mail (SMTP) |
| Güvenlik | reCAPTCHA, `.env` tabanlı kimlik bilgileri |
| Ön yüz | HTML, CSS, Bootstrap |

## Dizin Yapısı

```
ovasan-website/
├── run.py                     # Giriş noktası
├── config.py                  # Yapılandırma (.env tabanlı)
├── requirements.txt
└── app/
    ├── __init__.py            # Uygulama fabrikası
    ├── extensions.py          # MySQL, Mail eklentileri
    ├── controllers/           # main / auth / admin
    ├── models/                # Veritabanı işlemleri
    ├── data/                  # Statik içerik verileri
    ├── utils/                 # auth, mail, admin, log yardımcıları
    ├── templates/             # Jinja2 şablonları
    └── static/                # CSS, JS, görseller
```

## Kurulum

Gereksinimler: **Python 3.10+** ve **MySQL 5.7+/8+**.

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

mysql -u root -p -e "CREATE DATABASE ovasan CHARACTER SET utf8mb4;"

cp .env.example .env          # değerleri düzenleyin
python run.py
```

Uygulama `http://localhost:5000` üzerinde açılır.

## Ortam Değişkenleri

`.env` içinde: `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`,
`SECRET_KEY`, `PANEL_USERNAME`, `PANEL_PASSWORD`, `MAIL_USERNAME`,
`MAIL_PASSWORD`, `MAIL_RECIPIENTS`, `RECAPTCHA_SITE_KEY`.

> Gmail kullanıyorsanız normal şifre yerine **uygulama şifresi** oluşturun.

## Yönetim Paneli

`/login` adresinden `.env` içindeki `PANEL_USERNAME` / `PANEL_PASSWORD` ile giriş yapılır.

## Lisans

MIT — bkz. [LICENSE](LICENSE).