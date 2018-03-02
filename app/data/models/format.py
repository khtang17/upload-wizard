from app import db


class FileFormat(db.Model):
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

    def __repr__(self):
        return '<FileFormat {}>'.format(self.title)


