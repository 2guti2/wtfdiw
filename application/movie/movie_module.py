from application.movie.controllers.movie_controller import configure_movie_views


def configure_movie_module(app):
    configure_movie_views(app)
