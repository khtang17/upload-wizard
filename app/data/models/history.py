from datetime import datetime
from app import db
from flask_user import current_user
from app.data.models.job_log import JobLogModel
from app.data.models.catalog_info import CatalogResultInfo
from app.data.models.status import StatusModel
from flask import url_for, jsonify
from sqlalchemy import extract





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
        # resources = query.paginate(page, per_page, False)
        data = {
            'data': [item.to_dict() for item in query.all()],
            'meta': {
                'page': page,
                'perpage': per_page,
                # 'pages': resources.pages,
                # 'total': resources.total,
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
    catalog_type = db.Column(db.String(50))
    upload_type = db.Column(db.String(50))
    availability = db.Column(db.String(50))
    last_updated = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # natural_products = db.Column(db.Boolean(), nullable=False, default=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'), default=1)
    data_array = db.Column(db.Text, nullable=True)
    completion_emailed = db.Column(db.Boolean(), nullable=True, default=False)
    job_logs = db.relationship(JobLogModel,
                               order_by='asc(JobLogModel.date)',
                               backref='history',
                               lazy='dynamic')
    result_info = db.relationship(CatalogResultInfo,
                              backref='catalog_result',
                              lazy='dynamic')


    def create_shortname(self):
        basename = current_user.short_name
        # catalog type
        if self.catalog_type == 'sc' or self.catalog_type == 'mixed':
            shortname = basename
        else:
            shortname = basename + self.catalog_type
        # availability
        if self.upload_type == 'demand':
            shortname += '-v'
        return shortname


    @classmethod
    def get_last_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.id.desc()).first()

    @classmethod
    def get_all_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.id.desc()).all()

    def to_dict(self):
        data = {
            'ID': self.id,
            'UserId': self.user_id,
            'DateUploaded': self.date_uploaded.isoformat() + 'Z',
            'FileName': self.file_name,
            'FileSize': self.file_size,
            'CatalogType': self.catalog_type,
            'UploadType': self.upload_type,
            'Availability': self.availability,
            # 'NaturalProducts': self.natural_products,
            'StatusId': self.status_id,
            'LatestUpdated': self.last_updated.isoformat() + 'Z'
            # 'Status': self.get_status_type()
        }
        return data

    @classmethod
    def get_this_month_upload(cls):
        this_month = datetime.today().month
        this_month_histories = cls.query.filter(extract('month', cls.date_uploaded) == this_month).all()
        return this_month_histories


    def from_dict(self, data):
        for field in ['id', 'user_id', 'date_uploaded']:
            if field in data:
                setattr(self, field, data[field])

    def __init__(self, user_id, file_name, file_size):
        self.user_id = user_id
        # self.file_name = "{}_{}".format(self.get_miliseconds(), file_name.replace(" ", "_"))
        self.file_name = file_name
        self.file_size = file_size

    def get_status_type(self):
        job = self.job_logs.order_by(JobLogModel.status_type.desc()).first()
        if job:
            return job.status_type
        return 4
    def modify_status(self, new_status):
        self.status_id = new_status
        self.last_updated = datetime.utcnow
        db.session.commit()

    def json(self):
        shortname = self.create_shortname()
        return {'id': self.id,
                'user_id': self.user_id,
                'company_basename' : current_user.short_name,
                'short_name' : shortname,
                # 'date_uploaded': self.date_uploaded.isoformat() + 'Z',
                'file_name': self.file_name,
                'file_size': self.file_size,
                'catalog_type': self.catalog_type,
                'upload_type' : self.upload_type,
                'availability': self.availability,
                # 'natural_products': self.natural_products,
                }

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

    @classmethod
    def check_email_notify(seft):
        try:
            from app.email import notify_job_result_to_user
            if seft.status_id == 11:
                if seft.user.company.job_notify_email:
                    notify_job_result_to_user(seft)
        except:
            pass

    def __repr__(self):
        return '<UploadHistory id: {} filename : {}>'.format(self.id, self.file_name)

    # def get_status(self):
    #     status_msg = StatusModel.query.join()

    def __str__(self):
        return str(self.id)

