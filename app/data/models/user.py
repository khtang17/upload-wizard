from app import db

from werkzeug.security import generate_password_hash, check_password_hash

from flask_security import UserMixin, RoleMixin
from flask_user import UserMixin
from app.data.models.history import UploadHistoryModel
from sqlalchemy import event


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
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime, index=True)
    upload_histories = db.relationship(UploadHistoryModel, backref='user', lazy='dynamic')
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    roles = db.relationship('RoleModel', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    # def __init__(self, username, email, password, active):
    #     self.email = email
    #     self.username = username
    #     self.password = password
    #     self.active = False

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)

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


def my_append_listener(target, value, initiator):
    from app.email import notify_new_role_to_user
    notify_new_role_to_user(target)
    if str(value).startswith("Vendor"):
        # notify_new_role_to_user()
        pass


event.listen(UserModel.roles, 'append', my_append_listener)
