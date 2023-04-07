from app.users.models import User


def user_loader(header, payload):
    identity = payload['sub']
    return User.query.filter_by(id=identity).one_or_none()


def expired_token_loader(header, payload):
    return {'message': 'The access token has expired'}, 401


def unauthorized_loader(reason):
    return {'message': reason}, 401
