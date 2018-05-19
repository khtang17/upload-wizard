from app import db


class CatalogModel(db.Model):
    __tablename__ = 'catalog'

    id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String(100), index=True)
    type = db.Column(db.String(100), index=True)
    value = db.Column(db.String(500), index=True)
    value2 = db.Column(db.String(500), index=True)
    history_id = db.Column(db.Integer, db.ForeignKey('history.id'))

    def __init__(self, field_name, type, value, history_id):
        self.field_name = field_name
        self.type = type
        self.value = value
        self.history_id = history_id

    @classmethod
    def find_by_history_id(cls, id):
        return cls.query.filter_by(history_id=id).order_by(cls.id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()