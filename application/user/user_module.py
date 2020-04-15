import json
import requests
from application.factories.socketio import socket_io
from application.factories.oauth_client import oauth
from application.user.models.session_model import Session
from application.user.models.user_model import User
from application.user.services.google_service import GoogleService
from application.user.services.session_service import SessionService
from application.user.services.user_service import UserService
from application.user.controllers.session_controller import configure_session_views
from application.user.controllers.user_controller import configure_user_views
from application.user.controllers.socket_controller import configure_sockets
from flask_socketio import SocketIO
from injector import singleton


def configure_user_module(app, db, binder):
    google_service_instance = GoogleService(app, json, oauth, requests)
    user_service_instance = UserService(db, User)
    session_service_instance = SessionService(
        db, Session, User, google_service_instance, user_service_instance
    )

    binder.bind(GoogleService, to=google_service_instance, scope=singleton)
    binder.bind(UserService, to=user_service_instance, scope=singleton)
    binder.bind(SessionService, to=session_service_instance, scope=singleton)
    binder.bind(SocketIO, to=socket_io, scope=singleton)

    configure_user_views(app)
    configure_session_views(app)
    configure_sockets()
