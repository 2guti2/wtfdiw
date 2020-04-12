class OauthService:

    @staticmethod
    def get_redirect_url(client_id, args):
        app, oauth, request, callback_uri = args

        google_provider_cfg = oauth.get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg['authorization_endpoint']
        callback_url = build_callback_url(request, callback_uri)

        return oauth.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=callback_url,
            scope=['openid', 'email', 'profile'],
            state=client_id
        )

    @staticmethod
    def get_user_info_from_google(code, args):
        app, json, oauth, request, requests = args

        google_provider_cfg = oauth.get_google_provider_cfg()
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

        unique_id = user_info_response.json()['sub']
        users_email = user_info_response.json()['email']
        picture = user_info_response.json()['picture']
        users_name = user_info_response.json()['given_name']

        return unique_id, users_name, users_email, picture


def build_callback_url(req, callback_uri):
    base_url = req.base_url
    split_url = base_url.split('/')
    return 'https://' + split_url[2] + callback_uri
