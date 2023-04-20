from datetime import timedelta


class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    UPLOAD_DIR = '/nfs/general'


class ProductionConfig(Config):
    JWT_SECRET_KEY = 'ThVmYq3t6w9z$C&F)J@NcRfUjXnZr4u7'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@db:5432/conversion_tool'
    CELERY = dict({
        'broker_url': 'redis://redis:6379',
        'result_backend': 'redis://redis:6379',
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
