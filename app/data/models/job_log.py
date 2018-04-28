from app import db
from datetime import datetime


class JobLogModel(db.Model):
    __tablename__ = 'job_log'
    id = db.Column(db.Integer(), primary_key=True)
    history_id = db.Column(db.Integer, db.ForeignKey('history.id'))
    status = db.Column(db.String(1000))
    status_type = db.Column(db.String(255))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, history_id, status, status_type):
        self.history_id = history_id
        self.status = status
        self.status_type = status_type
