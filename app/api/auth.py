from flask import g
from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPTokenAuth
from app.data.models.user import UserModel
from app.api.errors import error_response
from passlib.hash import bcrypt_sha256
from passlib.hash import bcrypt

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = UserModel.query.filter_by(username=username).first()
    if user is None:
        return False
    else:
        g.current_user = user
        return bcrypt.verify(password, user.password)


@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)


@token_auth.verify_token
def verify_token(token):
    g.current_user = UserModel.check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    return error_response(401)
