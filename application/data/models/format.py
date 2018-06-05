from application import db


class FileFormatModel(db.Model):
    __tablename__ = 'file_format'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    col_type = db.Column(db.String(100))
    mandatory = db.Column(db.Boolean, unique=False, default=False)
    # separator = db.Column(db.String(10))
    order = db.Column(db.Integer, index=True)

    def __init__(self, title, col_type, order):
        self.title = title
        self.col_type = col_type
        self.order = order

    @classmethod
    def find_all(cls):
        return cls.query.order_by(cls.order).all()

    @classmethod
    def find_all_column_str(cls):
        str_cols = ""
        for idx, input_format in enumerate(cls.query.order_by(cls.order).all()):
            str_cols += input_format.title + ","
        return str_cols

    @classmethod
    def find_all_mandatory_column_str(cls):
        str_cols = ""
        for idx, input_format in enumerate(cls.query.filter_by(mandatory=True).order_by(cls.order).all()):
            str_cols += input_format.title + ","
        return str_cols

    @classmethod
    def find_all_optional_column_str(cls):
        str_cols = ""
        for idx, input_format in enumerate(
                cls.query.filter(FileFormatModel.mandatory.isnot(True)).order_by(cls.order).all()):
            str_cols += input_format.title + ","
        return str_cols

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<FileFormat {}>'.format(self.title)


