from flask_sqlalchemy import SQLAlchemy
from injector import Module, singleton
from application.factories.database import db, migrate
from application.user.user_module import configure_user_module


class AppModule(Module):
    def __init__(self, app):
        self.app = app

    def configure(self, binder):
        db_instance = self.configure_db(self.app)
        binder.bind(SQLAlchemy, to=db_instance, scope=singleton)
        configure_user_module(self.app, db_instance, binder)

    # noinspection PyMethodMayBeStatic
    def configure_db(self, app):
        db.init_app(app)
        migrate.init_app(app, db)
        return db
