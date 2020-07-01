import requests


class MovieApiService:
    def __init__(self, app):
        self.movie_api_base_url = app.config.get('MOVIE_API_BASE_URL')
        self.movie_api_key = app.config.get('MOVIE_API_KEY')
        self.default_lang = 'en'

    def get_genres(self):
        url = f'{self.movie_api_base_url}/genre/movie/list'
        querystring = {
            'api_key': self.movie_api_key,
            'language': self.default_lang
        }

        response = requests.request('GET', url, params=querystring)
        return response

    def get_movies(self):
        url = f'{self.movie_api_base_url}/movie/popular'
        querystring = {
            'api_key': self.movie_api_key,
            'language': self.default_lang,
            'page': 1
        }

        response = requests.request('GET', url, params=querystring)
        return response
