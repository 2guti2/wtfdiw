from flask import request
from application.factories.oauth_client import oauth
from application.factories.socketio import socket_io


def configure_sockets():
    @socket_io.on('client::user::connected')
    def on_client_connected(data):
        client_id = data['id']
        redirect_url = get_redirect_url(client_id, callback_uri='/sessions/callback')
        socket_io.emit(f"server::redirect::{client_id}", redirect_url)


def get_redirect_url(client_id, callback_uri):
    google_provider_cfg = oauth.get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']
    callback_url = build_callback_url(request, callback_uri)

    return oauth.client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=callback_url,
        scope=['openid', 'email', 'profile'],
        state=client_id
    )


def build_callback_url(req, callback_uri):
    base_url = req.base_url
    split_url = base_url.split('/')
    return f"https://{split_url[2]}{callback_uri}"
