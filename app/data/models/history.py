from datetime import datetime
from app import db
from app.data.models.job_log import JobLogModel
from app.data.models.catalog import CatalogModel
from flask import url_for


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, *endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'data': [item.to_dict() for item in resources.items],
            'meta': {
                'page': page,
                'perpage': per_page,
                'pages': resources.pages,
                'total': resources.total,
                'sort': "desc",
                'field': "DateUploaded"
            },
            'links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

    @staticmethod
    def to_all_collection_dict(query, page, per_page, field):
        resources = query.paginate(page, per_page, False)
        data = {
            'data': [item.to_dict() for item in query.all()],
            'meta': {
                'page': page,
                'perpage': per_page,
                'pages': resources.pages,
                'total': resources.total,
                'sort': "desc",
                'field': field
            }
        }
        return data


class UploadHistoryModel(PaginatedAPIMixin, db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_uploaded = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    file_name = db.Column(db.String(200))
    file_size = db.Column(db.String(200))
    type = db.Column(db.String(50))
    purchasability = db.Column(db.String(50))
    natural_products = db.Column(db.Boolean(), nullable=False)
    status = db.Column(db.Integer, index=True, nullable=False, default=1)
    job_logs = db.relationship(JobLogModel,
                               order_by='asc(JobLogModel.date)',
                               backref='history',
                               lazy='dynamic')

    catalogs = db.relationship(CatalogModel,
                               order_by='asc(CatalogModel.id)',
                               backref='history',
                               lazy='dynamic')

    def to_dict(self, include_email=False):
        data = {
            'ID': self.id,
            'UserId': self.user_id,
            'DateUploaded': self.date_uploaded.isoformat() + 'Z',
            'FileName': self.file_name,
            'FileSize': self.file_size,
            'Type': self.type,
            'Purchasability': self.purchasability,
            'NaturalProducts': self.natural_products,
            'Status': self.status,
        }
        return data

    def from_dict(self, data):
        for field in ['id', 'user_id', 'date_uploaded']:
            if field in data:
                setattr(self, field, data[field])

    def __init__(self, user_id, file_name, file_size):
        self.user_id = user_id
        self.file_name = "{}_{}".format(self.get_miliseconds(), file_name.replace(" ", "_"))
        self.file_size = file_size

    def json(self):
        return {'id': self.id,
                'user_id': self.user_id,
                # 'date_uploaded': self.date_uploaded.isoformat() + 'Z',
                'file_name': self.file_name,
                'file_size': self.file_size,
                'type': self.type,
                'purchasability': self.purchasability,
                'natural_products': self.natural_products,
                'status': self.status}

    def get_miliseconds(self):
        (dt, micro) = datetime.utcnow().strftime('%Y%m%d%H%M%S.%f').split('.')
        dt = "%s%03d" % (dt, int(micro) / 1000)
        return dt

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
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.date_uploaded).all()

    def __repr__(self):
        return '<UploadHistory {}>'.format(self.file_name)

