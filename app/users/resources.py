from flask import request
from flask_restful import Resource
from flask_expects_json import expects_json
from flask_jwt_extended import create_access_token

from app.database import db
from app.users.models import User, UserSchema
from app.users.schemas import login, sign_up


class Login(Resource):

    @expects_json(login)
    def post(self):
        username = request.json['username']
        password = request.json['password']

        user = User.query.filter_by(username=username).one_or_none()
        if not user or not user.check_password(password):
            return {'message': 'Wrong username or password'}, 401

        access_token = create_access_token(identity=user.id)
        return {'accessToken': access_token}, 200


class SignUp(Resource):

    @expects_json(sign_up)
    def post(self):
        username = request.json['username']
        password = request.json['password1']
        passwordConfirm = request.json['password2']
        email = request.json['email']

        if not password == passwordConfirm:
            return {'message': 'Passwords do not match'}, 400

        if User.query.filter_by(username=username).one_or_none():
            return {'message': f'User {username} is already registered'}, 400

        if User.query.filter_by(email=email).one_or_none():
            return {'message': f'Email {email} is already taken'}, 400

        password_hash = User.generate_hash(password)
        user = User(username=username, password=password_hash, email=email)
        db.session.add(user)
        db.session.commit()

        user_schema = UserSchema()
        return user_schema.dump(user), 201
