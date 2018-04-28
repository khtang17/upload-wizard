from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from app.data.models.history import UploadHistoryModel


class History(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('price',
    #                     type=float,
    #     required=True,
    #     help="This field cannot be left blank"
    # )
    # parser.add_argument('store_id',
    #     type=int,
    #     required=True,
    #     help="Every item needs a store id."
    # )

    # @jwt_required()
    def get(self, id):
        item = UploadHistoryModel.find_by_id(id)
        if item:
            return UploadHistoryModel.json()
        return {'message': 'History not found'}, 404


class HistoryList(Resource):
    def get(self):
        return {'histories1': [x.json() for x in UploadHistoryModel.query.all()]}
