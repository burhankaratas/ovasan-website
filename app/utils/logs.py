from flask import request
from datetime import datetime
import os

LOG_DIR = os.path.join("app", "logs")

def save_error(content):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    file_path = os.path.join(LOG_DIR, "error.log")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"{current_time}: '{content}'\n")


def save_http_request():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    file_path = os.path.join(LOG_DIR, "http_requests.log")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"{current_time}: '{request.method}' - {request.url}\n")