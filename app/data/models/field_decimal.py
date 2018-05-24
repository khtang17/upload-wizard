from app import db


class FieldDecimalModel(db.Model):
    __tablename__ = 'field_decimal'

    id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String(100), index=True, unique=True)
    min_val = db.Column(db.Float)
    max_val = db.Column(db.Float)
    decimal_places = db.Column(db.Integer)

    # def __init__(self, field_name, min_val, max_val, decimal_places):
    #     self.field_name = field_name
    #     self.min_val = min_val
    #     self.max_val = max_val
    #     self.decimal_places = decimal_places

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()