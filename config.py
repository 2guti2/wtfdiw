from os import environ, path
basedir = path.abspath(path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    RDS_USERNAME = environ.get('RDS_USERNAME')
    RDS_PASSWORD = environ.get('RDS_PASSWORD')
    RDS_HOSTNAME = environ.get('RDS_HOSTNAME')
    RDS_PORT = environ.get('RDS_PORT')
    RDS_DB_NAME = environ.get('RDS_DB_NAME')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{dbname}" \
        .format(username=RDS_USERNAME, password=RDS_PASSWORD, hostname=RDS_HOSTNAME, port=RDS_PORT, dbname=RDS_DB_NAME)
    GOOGLE_CLIENT_ID = environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = environ.get('GOOGLE_DISCOVERY_URL')
    MOVIE_API_BASE_URL = environ.get('MOVIE_API_BASE_URL')
    MOVIE_API_KEY = environ.get('MOVIE_API_KEY')


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True