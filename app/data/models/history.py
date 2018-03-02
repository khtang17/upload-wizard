from datetime import datetime
from app import db
from hashlib import md5


class UploadHistoryModel(db.Model):
    __tablename__ = 'histories'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_uploaded = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    file_name = db.Column(db.String(200))

    def __init__(self, user_id, file_name):
        self.user_id = user_id
        self.file_name = "{}_{}".format(md5(str.encode(str(datetime.utcnow))).hexdigest(), file_name)

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