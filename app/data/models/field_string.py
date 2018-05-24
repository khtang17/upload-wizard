from app import db


class FieldStringModel(db.Model):
    __tablename__ = 'field_string'

    id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String(100), index=True, unique=True)
    allowed_values = db.Column(db.Text)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
