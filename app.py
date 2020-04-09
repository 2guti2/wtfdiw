import os
import ssl
from flask import Flask
from werkzeug import run_simple
from login_manager import login_manager
from database import db, migrate
import views


def create_app():
    new_app = Flask(__name__)
    new_app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
    new_app.config.from_object(os.environ['APP_SETTINGS'])
    new_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(new_app)
    migrate.init_app(new_app, db)
    new_app.register_blueprint(views.app_bp, url_prefix='')
    new_app.register_blueprint(views.login_bp, url_prefix='')
    new_app.register_blueprint(views.logout_bp, url_prefix='')
    login_manager.init_app(new_app)
    return new_app


if __name__ == '__main__':
    app = create_app()
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctx.load_cert_chain('localhost.crt', 'localhost.key')
    run_simple('0.0.0.0', 5000, app, ssl_context=ctx)
