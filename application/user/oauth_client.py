from oauthlib.oauth2 import WebApplicationClient


class OauthClient:
    def __init__(self):
        self.client = None

    def init_app(self, app):
        self.client = WebApplicationClient(app.config.get('GOOGLE_CLIENT_ID'))


oauth = OauthClient()
