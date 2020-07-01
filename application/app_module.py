from flask_sqlalchemy import SQLAlchemy
from injector import Module, singleton
from application.factories.database import db, migrate
from application.movie.movie_module import configure_movie_module
from application.user.user_module import configure_user_module
from application.genre.genre_module import configure_genre_module
from application.movie_api.movie_api_service import MovieApiService


class AppModule(Module):
    def __init__(self, app):
        self.app = app

    def configure(self, binder):
        db_instance = self.configure_db(self.app)
        movie_api_service_instance = MovieApiService(self.app)
        binder.bind(SQLAlchemy, to=db_instance, scope=singleton)
        binder.bind(MovieApiService, to=movie_api_service_instance, scope=singleton)
        configure_user_module(self.app, db_instance, binder)
        configure_movie_module(self.app)
        configure_genre_module(self.app)

    # noinspection PyMethodMayBeStatic
    def configure_db(self, app):
        db.init_app(app)
        migrate.init_app(app, db)
        return db
