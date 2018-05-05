from app import db
from datetime import datetime
from sqlalchemy import and_


class JobLogModel(db.Model):
    __tablename__ = 'job_log'
    id = db.Column(db.Integer(), primary_key=True)
    history_id = db.Column(db.Integer, db.ForeignKey('history.id'))
    status = db.Column(db.Text)
    status_type = db.Column(db.Integer())
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # def __init__(self, history_id, status, status_type):
    #     self.history_id = history_id
    #     self.status = status
    #     self.status_type = status_type

    @classmethod
    def find_by_history(cls, history_id, job_id):
        return cls.query.filter(and_(cls.history_id == history_id, cls.id > job_id)).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def from_dict(self, data):
        for field in ['history_id', 'status', 'status_type']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'history_id': self.history_id,
            'status': self.status,
            'status_type': self.status_type
        }
        return data
