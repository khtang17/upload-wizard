from app import db


class FileFormatModel(db.Model):
    __tablename__ = 'file_format'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    col_type = db.Column(db.String(100))
    # mandatory = db.Column(db.Boolean)
    # separator = db.Column(db.String(10))
    order = db.Column(db.Integer, index=True)

    def __init__(self, title, col_type, order):
        self.title = title
        self.col_type = col_type
        self.order = order

    @classmethod
    def find_all(cls):
        return cls.query.order_by(cls.order).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<FileFormat {}>'.format(self.title)


