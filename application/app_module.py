import json
import requests
from flask_sqlalchemy import SQLAlchemy
from injector import Module, singleton
from application.factories.database import db, migrate
from application.factories.socketio import socket_io
from application.factories.oauth_client import oauth
from application.user.models.session_model import Session
from application.user.models.user_model import User
from application.user.services.google_service import GoogleService
from application.user.services.session_service import SessionService
from application.user.services.user_service import UserService
from flask_socketio import SocketIO


class AppModule(Module):
    def __init__(self, app):
        self.app = app

    def configure(self, binder):
        db_instance = self.configure_db(self.app)
        google_service_instance = GoogleService(self.app, json, oauth, requests)
        user_service_instance = UserService(db_instance, User)
        session_service_instance = SessionService(
            db_instance, Session, User, google_service_instance, user_service_instance
        )

        binder.bind(SQLAlchemy, to=db_instance, scope=singleton)
        binder.bind(GoogleService, to=google_service_instance, scope=singleton)
        binder.bind(UserService, to=user_service_instance, scope=singleton)
        binder.bind(SessionService, to=session_service_instance, scope=singleton)
        binder.bind(SocketIO, to=socket_io, scope=singleton)

    # noinspection PyMethodMayBeStatic
    def configure_db(self, app):
        db.init_app(app)
        migrate.init_app(app, db)
        return db
