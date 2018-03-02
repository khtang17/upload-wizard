from app import db


class FileFormat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    type = db.Column(db.String(100))
    mandatory = db.Column(db.Boolean)
    separator = db.Column(db.String(10))
    order = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<FileFormat {}>'.format(self.title)


