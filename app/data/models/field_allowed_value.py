from app import db


class FieldAllowedValueModel(db.Model):
    __tablename__ = 'field_allowed_value'

    id = db.Column(db.Integer, primary_key=True)
    allowed_values = db.Column(db.Text, nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'), nullable=False, unique=True)
    field = db.relationship("FieldModel", back_populates="field_allowed_value")

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
