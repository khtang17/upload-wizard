from app import db


class SettingsModel(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String(100), index=True)
    field_type = db.Column(db.String(100))
    min = db.Column(db.Float)
    max = db.Column(db.Float)
    number_of_decimal = db.Column(db.Integer)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
