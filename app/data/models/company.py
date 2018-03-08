from app import db
from app.data.models.user import UserModel
from datetime import datetime


class CompanyModel(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(400), index=True, unique=True)
    logo = db.Column(db.String(400))
    address = db.Column(db.String(100), index=True, unique=True)
    telephone_number = db.Column(db.String(40), index=True, unique=True)
    toll_free_number = db.Column(db.String(40), index=True, unique=True)
    fax_number = db.Column(db.String(40), index=True, unique=True)
    website = db.Column(db.String(100), index=True, unique=True)
    sales_email = db.Column(db.String(100), index=True, unique=True)
    date_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    users = db.relationship(UserModel, backref='company', lazy='dynamic')

    def __init__(self, name, description, address, telephone_number,
                 toll_free_number, fax_number, website, sales_email):
        self.name = name.upper()
        self.description = description
        self.logo = ""
        self.address = address
        self.telephone_number = telephone_number
        self.toll_free_number = toll_free_number
        self.fax_number = fax_number
        self.website = website
        self.sales_email = sales_email

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
