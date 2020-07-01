from application.genre.controllers.genre_controller import configure_genre_views


def configure_genre_module(app):
    configure_genre_views(app)
