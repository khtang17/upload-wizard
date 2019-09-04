from app import db



class StatusModel(db.Model):
    __tablename__ = 'status'
    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Text, nullable=False)

    # def __init__(self, status):
    #     self.status = status
    def __repr__(self):
        return '<Job Status {}>'.format(self.status)
    def __str__(self):
        return self.status

    def object_as_dict(self):
        return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

    @classmethod
    def to_dict(cls):
        # all_statuses =cls.query.all()
        #
        # statuses_dict = {}
        # for status in all_statuses:
        #     item = {status.status_id: status.status}
        #     statuses_dict.update(item)
        all_statuses = cls.query.all()
        statuses_dict = {}
        for status in all_statuses:
            item = {status.status_id : status.status}
            statuses_dict.update(item)
        return dict(statuses_dict)

    @classmethod
    def get_status_by_id(cls, status_id):
        status = cls.query.filter_by(status_id=status_id).first()
        return status