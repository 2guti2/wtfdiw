import os
from injector import Injector
from flask import Flask
from flask_injector import FlaskInjector
from flask_cors import CORS
from application.app_module import AppModule
from application.factories.socketio import socket_io
from application.factories.oauth_client import oauth
from application.user.controllers.session_controller import configure_session_views
from application.user.controllers.user_controller import configure_user_views
from application.user.controllers.socket_controller import configure_sockets


def setup_config(app):
    app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)
    app.config.from_object(os.environ['APP_SETTINGS'])
    oauth.init_app(app)


def setup_api(app):
    socket_io.init_app(app, cors_allowed_origins='*')
    CORS(app)
    injector = Injector([AppModule(app)])
    configure_user_views(app)
    configure_session_views(app)
    configure_sockets()
    FlaskInjector(app=app, injector=injector)


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    setup_config(app)
    setup_api(app)
    return app
