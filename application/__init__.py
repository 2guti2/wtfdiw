import os
from flask import Flask
from application.user.login_manager import login_manager
from application.database import db, migrate
from application.controllers import blueprints


def setup_config(app):
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
    app.config.from_object(os.environ['APP_SETTINGS'])


def setup_db(app):
    db.init_app(app)
    migrate.init_app(app, db)


def setup_api(app):
    for b in blueprints:
        app.register_blueprint(b)
    login_manager.init_app(app)


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    setup_config(app)
    setup_db(app)
    setup_api(app)
    return app
