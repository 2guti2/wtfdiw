import os
from flask import Flask
from application.login_manager import login_manager
from application.database import db, migrate
from application import views


def create_app():
    new_app = Flask(__name__, instance_relative_config=False)
    new_app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
    new_app.config.from_object(os.environ['APP_SETTINGS'])
    new_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(new_app)
    migrate.init_app(new_app, db)
    new_app.register_blueprint(views.app_bp, url_prefix='')
    new_app.register_blueprint(views.login_bp, url_prefix='')
    new_app.register_blueprint(views.logout_bp, url_prefix='')
    login_manager.init_app(new_app)
    return new_app
