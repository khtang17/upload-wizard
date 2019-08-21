from app import db
from app.data.models.user import UserModel
from datetime import datetime
from flask import current_app
from sqlalchemy import func


class CompanyModel(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(1024), index=True)
    logo = db.Column(db.String(400))
    address = db.Column(db.String(100), index=True)
    telephone_number = db.Column(db.String(40), index=True)
    toll_free_number = db.Column(db.String(40), index=True)
    fax_number = db.Column(db.String(40), index=True)
    website = db.Column(db.String(100), index=True)
    sales_email = db.Column(db.String(100), index=True)
    personal_contact_name = db.Column(db.String(100), index=True)
    personal_contact_email = db.Column(db.String(100), index=True)
    date_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    users = db.relationship(UserModel, backref='company', lazy='dynamic')
    idnumber = db.Column(db.String(100))
    cmpdname = db.Column(db.String(100))
    smiles = db.Column(db.String(100))
    cas = db.Column(db.String(100))
    price = db.Column(db.String(20))
    job_notify_email = db.Column(db.Boolean(), nullable=True, default=False)

    def __init__(self, name, description, address, telephone_number,
                 toll_free_number, fax_number, website, sales_email,
                 personal_contact_name, personal_contact_email,
                 idnumber, smiles, cmpdname, cas, price, job_notify_email):
        self.name = name
        self.description = description
        self.address = address
        self.telephone_number = telephone_number
        self.toll_free_number = toll_free_number
        self.fax_number = fax_number
        self.website = website
        self.sales_email = sales_email
        self.personal_contact_name = personal_contact_name
        self.personal_contact_email = personal_contact_email
        self.idnumber = idnumber
        self.smiles = smiles
        self.cmpdname = cmpdname
        self.cas = cas
        self.price = price
        self.job_notify_email = job_notify_email

    @property
    def url(self):
        if current_app.config["ZINC_MODE"]:
            return current_app.config['LOGO_UPLOAD_FOLDER_URL'] + self.logo
        else:
            return self.logo

    # @property
    # def zinc_filepath(self):
    #     if self.logo is None:
    #         return
    #     return current_app.config['LOGO_UPLOAD_FOLDER_URL'] + self.logo

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(func.lower(cls.name) == func.lower(name)).first()

    def __repr__(self):
        return '<Company {}>'.format(self.name)

    def __str__(self):
        return self.name




