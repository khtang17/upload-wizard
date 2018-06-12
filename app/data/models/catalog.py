from app import db
import time


class CatalogModel(db.Model):
    __tablename__ = 'catalog'

    id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String(100), index=True)
    type = db.Column(db.String(100))
    value = db.Column(db.String(500))
    history_id = db.Column(db.Integer, db.ForeignKey('history.id'))

    def __init__(self, field_name, type, value, history_id):
        self.field_name = field_name
        self.type = type
        self.value = value
        self.history_id = history_id

    @classmethod
    def find_by_history_id(cls, id):
        return cls.query.filter_by(history_id=id).order_by(cls.id).all()

    @classmethod
    def save_objects(cls, objects):
        t0 = time.time()
        db.session.bulk_save_objects(objects)
        db.session.commit()
        print(
            "SQLAlchemy ORM bulk_save_objects(): Total time for " +
            " records " + str(time.time() - t0) + " secs")

    @classmethod
    def save_mappings(cls, objects):
        t0 = time.time()
        db.session.bulk_insert_mappings(
            CatalogModel, objects
        )
        db.session.commit()
        print(
            "SQLAlchemy ORM bulk_save_objects(): Total time for " +
            " records " + str(time.time() - t0) + " secs")

    @classmethod
    def save_bulk(cls, objects):
        t0 = time.time()
        db.engine.execute(CatalogModel.__table__.insert(), objects)
        # db.session.commit()
        print(
            "SQLAlchemy ORM bulk_save_objects(): Total time for " +
            " records " + str(time.time() - t0) + " secs")

    @classmethod
    def save_in_one_transaction(cls, objects):
        t0 = time.time()
        for o in objects:
            db.session.add(o)
        db.session.commit()
        print(
            "SQLAlchemy ORM ONE TRANSCATION(): Total time for " +
            " records " + str(time.time() - t0) + " secs")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()