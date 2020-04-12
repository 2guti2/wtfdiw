import binascii
import os
import requests
import json
from flask import (jsonify, request, current_app as app)
from application.database import db
from application.user.session_model import Session
from application.user.user_model import User
from application.socketio import socket_io
from application.user.oauth_client import oauth
from flask.blueprints import Blueprint
from flask_socketio import emit

callback_uri = '/sessions/callback'

sessions_bp = Blueprint('/sessions', __name__)
users_bp = Blueprint('/users', __name__)


@socket_io.on('client::user::connected')
def on_client_subscribe(data):
    client_id = data['id']
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    callback_url = build_callback_url(request)
    request_uri = oauth.client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=callback_url,
        scope=['openid', 'email', 'profile'],
        state=client_id
    )

    emit('server::redirect::' + client_id, request_uri)


@sessions_bp.route(callback_uri)
def session_callback():
    client_id = request.args.get('state')
    code = request.args.get('code')

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']

    token_url, headers, body = oauth.client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config.get('GOOGLE_CLIENT_ID'), app.config.get('GOOGLE_CLIENT_SECRET')),
    )

    oauth.client.parse_request_body_response(json.dumps(token_response.json()))

    user_info_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = oauth.client.add_token(user_info_endpoint)
    user_info_response = requests.get(uri, headers=headers, data=body)

    if user_info_response.json().get('email_verified'):
        unique_id = user_info_response.json()['sub']
        users_email = user_info_response.json()['email']
        picture = user_info_response.json()['picture']
        users_name = user_info_response.json()['given_name']
    else:
        return 'User email not available or not verified by Google.', 400

    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    db_user = User.query.filter_by(id=unique_id).first()
    exists = db_user is not None
    if not exists:
        db.session.add(user)
        db.session.commit()
    else:
        User.query.filter_by(id=unique_id).update(dict(id=unique_id, name=users_name, email=users_email, profile_pic=picture))
        db.session.commit()

    session = Session.query.filter_by(user_id=unique_id).first()
    exists = session is not None
    if not exists:
        session = Session(user_id_=unique_id, token=generate_key(), expiration=None)
        db.session.add(session)
        db.session.commit()

    response = {**user.serialize(), **session.serialize()}
    socket_io.emit('server::user::logged_in::' + client_id, response)

    return (
        '<script>window.close();</script>'
        '<p>Please close this tab</p>'
    )


@users_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users])


def get_google_provider_cfg():
    return requests.get(app.config.get('GOOGLE_DISCOVERY_URL')).json()


def build_callback_url(req):
    base_url = req.base_url
    split_url = base_url.split('/')
    return 'https://' + split_url[2] + callback_uri


def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()
