from datetime import datetime
from app import db


class UploadHistoryModel(db.Model):
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

    def __init__(self, user_id, file_name, file_size):
        self.user_id = user_id
        self.file_name = "{}_{}".format(self.get_miliseconds(), file_name)
        self.file_size = file_size

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
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.date_uploaded).all()

    def __repr__(self):
        return '<UploadHistory {}>'.format(self.file_name)