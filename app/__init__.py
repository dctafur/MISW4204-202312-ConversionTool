from os import environ, path
from flask import Flask, send_file
from flask_restful import Api
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException
from celery import Celery, Task

from app.config import config
from app.database import init_db
from app.users import Login, SignUp
from app.tasks import TaskCrud
from app.files import ReadFile
from app.utils.handlers import http_exception_handler
from app.utils.loaders import user_loader, expired_token_loader, unauthorized_loader


def create_app():
    config_name = environ.get('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_error_handler(HTTPException, http_exception_handler)

    init_db(app)
    init_celery_app(app)
    init_jwt_manager(app)
    init_restful_api(app)

    return app


def init_celery_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config['CELERY'])
    celery_app.set_default()
    app.extensions["celery"] = celery_app

    return celery_app


def init_jwt_manager(app):
    jwt = JWTManager(app)
    jwt.user_lookup_loader(user_loader)
    jwt.expired_token_loader(expired_token_loader)
    jwt.invalid_token_loader(unauthorized_loader)
    jwt.unauthorized_loader(unauthorized_loader)


def init_restful_api(app):
    def output_file(data, code, headers):
        file_name = data['file_name']
        upload_dir = path.join(path.dirname(app.root_path), app.config['UPLOAD_DIR'])
        file_path = f'{upload_dir}/{file_name}'
        return send_file(file_path, as_attachment=True)

    api = Api(app, prefix='/api')
    api.representations['application/octet-stream'] = output_file
    api.add_resource(Login, '/auth/login')
    api.add_resource(SignUp, '/auth/signup')
    api.add_resource(TaskCrud, '/tasks', '/tasks/<id>')
    api.add_resource(ReadFile, '/files/<file_name>')
