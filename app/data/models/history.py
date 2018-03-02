from datetime import datetime
from app import db


class UploadHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_uploaded = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    file_name = db.Column(db.String(200))

    def __repr__(self):
        return '<UploadHistory {}>'.format(self.file_name)