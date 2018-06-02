from app import db


class FieldModel(db.Model):
    __tablename__ = 'field'

    id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String(100), index=True, unique=True)
    mandatory = db.Column(db.Boolean, unique=False, default=False)
    field_decimal = db.relationship("FieldDecimalModel", uselist=False, back_populates="field")
    field_allowed_value = db.relationship("FieldAllowedValueModel", uselist=False, back_populates="field")

    @classmethod
    def find_by_mandatory(cls, mandatory):
        return cls.query.filter_by(mandatory=mandatory).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __str__(self):
        return self.field_name

    def __repr__(self):
        return '<Field {}>'.format(self.field_name)