from application import db


class FieldDecimalModel(db.Model):
    __tablename__ = 'field_decimal'

    id = db.Column(db.Integer, primary_key=True)
    min_val = db.Column(db.Float, nullable=False)
    max_val = db.Column(db.Float, nullable=False)
    decimal_places = db.Column(db.Integer, nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'), nullable=False, unique=True)
    field = db.relationship("FieldModel", back_populates="field_decimal")

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