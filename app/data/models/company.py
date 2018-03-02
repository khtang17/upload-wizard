from app import db


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    users = db.relationship('User', backref='company', lazy='dynamic')

    def __repr__(self):
        return '<Company {}>'.at(self.name)