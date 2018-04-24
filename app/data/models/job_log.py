from app import db
from datetime import datetime


class JobLogModel(db.Model):
    __tablename__ = 'job_log'
    id = db.Column(db.Integer(), primary_key=True)
    status = db.Column(db.String(1000))
    type = db.Column(db.String(255))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, id, status, type):
        self.id = id
        self.status = status
        self.type = type