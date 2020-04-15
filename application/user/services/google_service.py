class GoogleService:
    def __init__(self, app, json, oauth, requests):
        self.app = app
        self.json = json
        self.oauth = oauth
        self.requests = requests

    def get_user_info(self, code, request):
        google_provider_cfg = self.oauth.get_google_provider_cfg()
        token_endpoint = google_provider_cfg['token_endpoint']

        token_url, headers, body = self.oauth.client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code,
        )
        token_response = self.requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(self.app.config.get('GOOGLE_CLIENT_ID'), self.app.config.get('GOOGLE_CLIENT_SECRET')),
        )

        self.oauth.client.parse_request_body_response(self.json.dumps(token_response.json()))

        user_info_endpoint = google_provider_cfg['userinfo_endpoint']
        uri, headers, body = self.oauth.client.add_token(user_info_endpoint)
        user_info_response = self.requests.get(uri, headers=headers, data=body)

        unique_id = user_info_response.json()['sub']
        users_email = user_info_response.json()['email']
        picture = user_info_response.json()['picture']
        users_name = user_info_response.json()['given_name']

        return unique_id, users_name, users_email, picture
