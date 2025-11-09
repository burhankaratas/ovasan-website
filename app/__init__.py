from flask import Flask
from config import Config
from app.extensions import mysql
from app.extensions import mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)
    mail.init_app(app)

    from app.controllers.main_controller import main
    from app.controllers.auth_controller import auth
    from app.controllers.admin_controller import admin

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin)

    return app