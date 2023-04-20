from os import environ, path
from dotenv import load_dotenv
from datetime import timedelta

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    UPLOAD_DIR = '/nfs/general'


class ProductionConfig(Config):
    JWT_SECRET_KEY = 'ThVmYq3t6w9z$C&F)J@NcRfUjXnZr4u7'
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{environ.get('DB_USERNAME')}:{environ.get('DB_PASSWORD')}@{environ.get('DB_HOST')}:{environ.get('DB_PORT')}/{environ.get('DB_DATABASE')}"
    CELERY = dict({
        'broker_url': 'redis://127.0.0.1:6379',
        'result_backend': 'redis://127.0.0.1:6379',
    })


class DevelopmentConfig(Config):
    TESTING = True
    JWT_SECRET_KEY = '@NcQfTjWnZr4u7x!A%D*G-KaPdSgUkXp'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    CELERY = dict({
        'broker_url': 'redis://localhost:6379',
        'result_backend': 'redis://localhost:6379',
    })


config = {'production': ProductionConfig, 'development': DevelopmentConfig}
