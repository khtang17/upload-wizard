from app import db
from app.data.models.user import UserModel


class CompanyModel(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    users = db.relationship(UserModel, backref='company', lazy='dynamic')

    def __init__(self, name):
        self.name = name.upper()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name.upper()).first()

    def __repr__(self):
        return '<Company {}>'.format(self.name)
