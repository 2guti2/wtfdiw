import requests
import json
from flask import (jsonify, request)
from application.database import db
from application.user.models.session_model import Session
from application.user.services.session_service import SessionService
from application.user.models.user_model import User
from application.socketio import socket_io
from application.user.auth.oauth_client import oauth
from flask.blueprints import Blueprint
from application.user.services.oauth_service import OauthService
from application.user.services.user_service import UserService

callback_uri = '/sessions/callback'


def configure_views(app):
    sessions_bp = Blueprint('/sessions', __name__)
    users_bp = Blueprint('/users', __name__)

    @socket_io.on('client::user::connected')
    def on_client_connected(data):
        client_id = data['id']

        request_uri = OauthService.get_redirect_url(client_id, (
            app, oauth, request, callback_uri
        ))

        socket_io.emit('server::redirect::' + client_id, request_uri)

    @sessions_bp.route(callback_uri)
    def session_callback(user_service: UserService):
        client_id = request.args.get('state')
        code = request.args.get('code')

        response = \
            SessionService.new_session(
                code,
                (app, json, db, Session, User, OauthService, user_service, oauth, request, requests)
            )
        socket_io.emit('server::user::logged_in::' + client_id, response)

        return (
            '<script>window.close();</script>'
            '<p>Please close this tab</p>'
        )

    @users_bp.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify([u.serialize() for u in users])

    app.register_blueprint(users_bp)
    app.register_blueprint(sessions_bp)
