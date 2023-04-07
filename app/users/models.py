from hashlib import sha256
from sqlalchemy.sql import func

from app.database import db, ma
from app.tasks.models import Task


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    tasks = db.relationship('Task', backref='user', lazy=True)

    @staticmethod
    def generate_hash(password):
        return sha256(password.encode('utf-8')).hexdigest()

    def check_password(self, password):
        hash = User.generate_hash(password)
        return hash == self.password


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    created_at = ma.auto_field()
