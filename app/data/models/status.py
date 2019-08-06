from app import db



class StatusModel(db.Model):
    __tablename__ = 'status'
    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Text, nullable=False)

    def __init__(self, status_id, status):
        self.status_id = status_id
        self.status = status
    @classmethod
    def to_dict(cls):
        # all_statuses =self.query.all()
        # statuses_dict = {}
        # for status in all_statuses:
        #     item = {status.status_id: status.status}
        #     statuses_dict.update(item)
        all_statuses = cls.query.all()
        statuses_dict = {}
        for status in all_statuses:
            item = {status.status_id : status.status}
            statuses_dict.update(item)
        return statuses_dict

    @classmethod
    def get_status_by_id(cls, status_id):
        status = cls.query.filter_by(status_id=status_id).first()
        return status