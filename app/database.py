from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


def init_db(app):
    with app.app_context():
        db.init_app(app)
        ma.init_app(app)
        db.create_all()
