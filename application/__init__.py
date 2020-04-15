import os
from injector import Injector
from flask import Flask
from flask_injector import FlaskInjector
from flask_cors import CORS
from application.app_module import AppModule
from application.factories.socketio import socket_io
from application.factories.oauth_client import oauth


def setup_config(app):
    app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)
    app.config.from_object(os.environ['APP_SETTINGS'])
    oauth.init_app(app)


def setup_app(app):
    socket_io.init_app(app, cors_allowed_origins='*')
    CORS(app)
    injector = Injector([AppModule(app)])
    FlaskInjector(app=app, injector=injector)


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    setup_config(app)
    setup_app(app)
    return app
