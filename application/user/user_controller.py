import os
import sys
import requests
import json
from flask import jsonify
from flask import request
from application.database import db
from application.user.user_model import User
from flask.blueprints import Blueprint
from oauthlib.oauth2 import WebApplicationClient
from application.socketio import socket_io
from flask_socketio import emit

callback_uri = '/sessions/callback'

sessions_bp = Blueprint('/sessions', __name__)
users_bp = Blueprint('/users', __name__)

client = WebApplicationClient(os.environ.get('GOOGLE_CLIENT_ID'))


@socket_io.on('client::subscribe')
def on_client_subscribe(data):
    client_id = data['id']
    print('new client connected, client_id: ' + str(client_id), file=sys.stderr)
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    callback_url = build_callback_url(request)
    request_uri = client.prepare_request_uri(
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

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(os.environ.get('GOOGLE_CLIENT_ID'), os.environ.get('GOOGLE_CLIENT_SECRET')),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    user_info_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = client.add_token(user_info_endpoint)
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

    response = user.serialize()

    db_user = User.query.filter_by(id=unique_id).first()
    exists = db_user is not None
    if not exists:
        db.session.add(user)
        db.session.commit()
    else:
        User.query.filter_by(id=unique_id).update(dict(id=unique_id, name=users_name, email=users_email, profile_pic=picture))
        db.session.commit()

    socket_io.emit('server::user::' + client_id, response)
    return (
        '<script>window.close();</script>'
        '<p>Please close this tab</p>'
    )


@users_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users])


def get_google_provider_cfg():
    return requests.get(os.environ.get('GOOGLE_DISCOVERY_URL')).json()


def build_callback_url(req):
    base_url = req.base_url
    split_url = base_url.split('/')
    return 'https://' + split_url[2] + callback_uri
