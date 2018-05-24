from app import db
from datetime import datetime
from sqlalchemy import and_


class JobLogModel(db.Model):
    __tablename__ = 'job_log'
    id = db.Column(db.Integer(), primary_key=True)
    history_id = db.Column(db.Integer, db.ForeignKey('history.id'))
    status = db.Column(db.Text)
    status_type = db.Column(db.Integer(), index=True)
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
        self.check_email_notify()

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

    def check_email_notify(self):
        from app.email import notify_job_result_to_user
        from app.data.models.history import UploadHistoryModel
        if self.status_type == 4:
            history = UploadHistoryModel.find_by_id(self.history_id)
            if history.user.company.job_notify_email:
                notify_job_result_to_user(history)

    def __str__(self):
        return self.status_type

    def __repr__(self):
        return '<JobLog history_id:{}, status_type{}>'.format(self.history_id, self.status_type)