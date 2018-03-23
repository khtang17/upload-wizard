from app import db
from app.data.models.user import UserModel
from datetime import datetime


class CompanyModel(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(400), index=True)
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
    idnumber = db.Column(db.String(20), default='IDNUMBER')
    cmpdname = db.Column(db.String(20), default='NAME')
    cas = db.Column(db.String(20))
    price = db.Column(db.String(20))

    def __init__(self, name, description, address, telephone_number,
                 toll_free_number, fax_number, website, sales_email,
                 personal_contact_name, personal_contact_email,
                 idnumber, cmpdname, cas, price):
        self.name = name.upper()
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
        self.cmpdname = cmpdname
        self.cas = cas
        self.pricae = price

    @property
    def url(self):
        from app import app
        return app.config['LOGO_UPLOAD_FOLDER_URL'] + self.logo

    @property
    def filepath(self):
        from app import app
        if self.logo is None:
            return
        return app.config['LOGO_UPLOAD_FOLDER_URL'] + self.logo

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
        return cls.query.filter_by(name=name.upper()).first()

    def __repr__(self):
        return '<Company {}>'.format(self.name)

    def __str__(self):
        return self.name
