import flask
from flask.blueprints import Blueprint
from application.movie_api.movie_api_service import MovieApiService


def configure_movie_views(app):
    movies_bp = Blueprint('/movies', __name__)

    @movies_bp.route('/movies', methods=['GET'])
    def get_movies(movie_service: MovieApiService):
        response = movie_service.get_movies()
        resp = flask.Response(response.text)
        resp.headers['Content-Type'] = 'application/json'
        return resp

    app.register_blueprint(movies_bp)
