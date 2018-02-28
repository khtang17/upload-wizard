from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    upload_histories = db.relationship('UploadHistory', backref='user', lazy='dynamic')
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class UploadHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_uploaded = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    file_name = db.Column(db.String(200))

    def __repr__(self):
        return '<UploadHistory {}>'.format(self.file_name)


class FileFormat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    type = db.Column(db.String(100))
    mandatory = db.Column(db.Boolean)
    separator = db.Column(db.String(10))
    order = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<FileFormat {}>'.format(self.title)


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    users = db.relationship('User', backref='company', lazy='dynamic')

    def __repr__(self):
        return '<Company {}>'.format(self.name)
