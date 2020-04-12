import os
import sys
import requests
import json
from flask import jsonify
from flask import redirect, request, url_for
from application.database import db
from application.user.user_model import User
from flask.blueprints import Blueprint
from application.user.login_manager import login_manager
from oauthlib.oauth2 import WebApplicationClient
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from application.socketio import socket_io
from flask_socketio import emit

clients = []

app_bp = Blueprint('/', __name__)
login_bp = Blueprint('/login', __name__)
logout_bp = Blueprint('/logout', __name__)
users_bp = Blueprint('/users', __name__)

client = WebApplicationClient(os.environ.get('GOOGLE_CLIENT_ID'))


def build_callback_url(request):
    base_url = request.base_url
    split_url = base_url.split('/')
    return 'https://' + split_url[2] + '/login/callback'


@socket_io.on('client::subscribe')
def on_client_subscribe(data):
    client_id = data['id']
    print('client_id: ' + str(client_id), file=sys.stderr)
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    callback_url = build_callback_url(request)
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=callback_url,
        scope=['openid', 'email', 'profile'],
    )

    print('request_uri: ' + str(request_uri), file=sys.stderr)
    emit('server::redirect::' + client_id, request_uri)


@users_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users])


@login_manager.unauthorized_handler
def unauthorized():
    return 'You must be logged in to access this content.', 403


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


@app_bp.route('/')
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'


@login_bp.route('/login')
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile'],
    )
    return redirect(request_uri)


@login_bp.route('/login/callback')
def callback():
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

    exists = User.query.filter_by(id=unique_id).first() is not None
    if not exists:
        db.session.add(user)
        db.session.commit()

    login_user(user)

    return redirect(url_for('/.index'))


@logout_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('/.index'))


def get_google_provider_cfg():
    return requests.get(os.environ.get('GOOGLE_DISCOVERY_URL')).json()
