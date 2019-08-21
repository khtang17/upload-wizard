from app import db

from flask_security import UserMixin, RoleMixin
from flask_user import UserMixin
from app.data.models.history import UploadHistoryModel
# from app.data.models.task import TaskModel
from sqlalchemy import event

import base64
from datetime import datetime, timedelta
import os
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time
from passlib.hash import bcrypt
from itsdangerous import URLSafeTimedSerializer

# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class RoleModel(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class UserModel(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    short_name = db.Column(db.String(64), index=True, nullable=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime, index=True)
    upload_histories = db.relationship(UploadHistoryModel,
                                       order_by='desc(UploadHistoryModel.date_uploaded)',
                                       backref='user',
                                       lazy='dynamic')
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    roles = db.relationship('RoleModel', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __init__(self, username, email):
        self.email = email
        self.username = username

    def set_password(self, password):
        self.password = bcrypt.encrypt(password)

    def check_password(self, password):
        return bcrypt.verify(self.password, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_admins(cls):
        return cls.query.filter(UserModel.roles.any(RoleModel.name.startswith('Admin'))).all()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email.lower()).first()

    def __str__(self):
        return self.username

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        db.session.commit()
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = UserModel.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return UserModel.query.get(id)

    def generate_confirmation_token(self):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(self.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=current_app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except:
            return False
        return email


def my_append_listener(target, value, initiator):
    from app.email import notify_new_role_to_user
    print(value)
    if str(value).startswith("Vendor"):
        notify_new_role_to_user(target)


event.listen(UserModel.roles, 'append', my_append_listener)


