import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def save_file(file, folder):
    """
    Gelen dosyayı kontrol eder, allowed uzantılardan mı diye bakar,
    ismini benzersiz hale getirir ve belirtilen folder altına kaydeder.
    """

    if not file:
        return False, "Dosya gönderilmedi."

    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[-1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        return False, "Dosya yalnızca PNG, JPG veya JPEG olabilir."

    unique_name = f"{uuid.uuid4().hex}.{ext}"

    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', folder)
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, unique_name)
    file.save(file_path)

    return True, unique_name
