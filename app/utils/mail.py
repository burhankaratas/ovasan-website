from flask import current_app
from flask_mail import Message

from app.extensions import mail


def send_mail(form_data, uploaded_file=None):
    try:
        sender = current_app.config.get("MAIL_USERNAME")
        recipients_raw = current_app.config.get("MAIL_RECIPIENTS", "burhankaratas771@gmail.com")
        recipients = [r.strip() for r in recipients_raw.split(",") if r.strip()]

        subject = "Ovasan Mühendislik Web Sitesi Mesajı"
        body = (
            "Yeni bir iletişim formu gönderimi var:\n\n"
            f"Kurum Adı: {form_data.get('kurum_name', '')}\n"
            f"Ad Soyad: {form_data.get('name', '')}\n"
            f"Telefon: {form_data.get('phone', '')}\n"
            f"E-posta: {form_data.get('email', '')}\n"
            f"Hizmet: {form_data.get('service', '')}\n"
            f"Mesaj: {form_data.get('message', '')}\n"
        )

        msg = Message(subject=subject, sender=sender, recipients=recipients, body=body)

        if uploaded_file and uploaded_file.filename:
            data = uploaded_file.read()
            content_type = uploaded_file.content_type or "application/octet-stream"
            msg.attach(filename=uploaded_file.filename, content_type=content_type, data=data)

        mail.send(msg)
        return True
    except Exception:
        return False
