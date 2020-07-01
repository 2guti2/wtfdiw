import flask
from flask.blueprints import Blueprint
from application.movie_api.movie_api_service import MovieApiService


def configure_genre_views(app):
    genres_bp = Blueprint('/selectGenre', __name__)

    @genres_bp.route('/selectGenre', methods=['GET'])
    def get_genres(movie_service: MovieApiService):
        response = movie_service.get_genres()
        resp = flask.Response(response.text)
        resp.headers['Content-Type'] = 'application/json'
        return resp

    app.register_blueprint(genres_bp)
