# from app import db
# from datetime import datetime
# from sqlalchemy import and_
# from app.data.models.history import UploadHistoryModel
#
# class CatalogResultInfo(db.Model):
#     __tablename__='catalog_info'
#     id = db.Column(db.Integer, index=True, autoincrement=True)
#     history_id = db.Column(db.Integer, db.ForeignKey('history.id'))
#     size = db.Column(db.Integer)
#     filtered = db.Column(db.Integer)
#     errors = db.Column(db.Integer)
#
#     # def __init__(self, history_id, size, filtered, errors):
#     #     self.history_id = history_id
#     #     self.size = size
#     #     self.filtered = filtered
#     #     self.errors = errors
#
#     def from_dict(self, data):
#         for field in ['history_id', 'size', 'filtered', 'errors']:
#             if field in data:
#                 setattr(self, field, data[field])
#
#     def to_dict(self):
#         data = {
#             'history_id': self.history_id,
#             'size': self.original_size,
#             'filtered': self.filtered,
#             'errors': self.errors
#         }
#         return data