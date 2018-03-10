from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
# from flask_login import UserMixin
from flask_security import UserMixin, RoleMixin
from app.data.models.history import UploadHistoryModel
from datetime import datetime

@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class RoleModel(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class UserModel(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    upload_histories = db.relationship(UploadHistoryModel, backref='user', lazy='dynamic')
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    roles = db.relationship('RoleModel', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, email, company_id):
        self.username = username
        self.email = email.lower()
        self.company_id = company_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email.lower()).first()

    def __repr__(self):
        return '<User {}>'.format(self.username)


