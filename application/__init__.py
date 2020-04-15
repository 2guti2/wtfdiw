import os
from flask import Flask
from flask_injector import FlaskInjector
from flask_sqlalchemy import SQLAlchemy
from injector import Module, singleton, Injector
from application.database import db, migrate
from application.socketio import socket_io
from flask_cors import CORS
from application.user.auth.oauth_client import oauth
from application.user.controllers.user_controller import configure_views
from application.user.models.user_model import User
from application.user.services.user_service import UserService


class AppModule(Module):
    def __init__(self, app):
        self.app = app

    def configure(self, binder):
        db_instance = self.configure_db(self.app)
        user_service_instance = UserService(db_instance, User)

        binder.bind(SQLAlchemy, to=db_instance, scope=singleton)
        binder.bind(UserService, to=user_service_instance, scope=singleton)

    # noinspection PyMethodMayBeStatic
    def configure_db(self, app):
        db.init_app(app)
        migrate.init_app(app, db)
        return db


def setup_config(app):
    app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)
    app.config.from_object(os.environ['APP_SETTINGS'])
    oauth.init_app(app)


def setup_db(app):
    db.init_app(app)
    migrate.init_app(app, db)


def setup_api(app):
    socket_io.init_app(app, cors_allowed_origins='*')
    CORS(app)
    injector = Injector([AppModule(app)])
    configure_views(app=app)
    FlaskInjector(app=app, injector=injector)


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    setup_config(app)
    setup_db(app)
    setup_api(app)
    return app
