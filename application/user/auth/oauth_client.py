from oauthlib.oauth2 import WebApplicationClient
import requests


class OauthClient:
    def __init__(self):
        self.client = None
        self.app_config = None

    def init_app(self, app):
        self.client = WebApplicationClient(app.config.get('GOOGLE_CLIENT_ID'))
        self.app_config = app.config

    def get_google_provider_cfg(self):
        return requests.get(self.app_config.get('GOOGLE_DISCOVERY_URL')).json()


oauth = OauthClient()
