from app.api import bp
from flask import jsonify
from app.data.models.history import UploadHistoryModel
from flask import request
from flask_login import current_user
from flask_user import login_required

# @bp.route('/history/<int:id>', methods=['GET'])
# def get_histories(id):
#     return jsonify(UploadHistoryModel.query.get_or_404(id).to_dict())


# @bp.route('/histories', methods=['GET', 'POST'])
# @login_required
# def get_histories():
#     page = request.args.get('page', 1, type=int)
#     per_page = min(request.args.get('per_page', 10, type=int), 100)
#     data = UploadHistoryModel.to_collection_dict(
#         UploadHistoryModel.query.filter_by(user_id=current_user.id), page, per_page, 'api.get_histories')
#         # UploadHistoryModel.query.filter_by(user_id=current_user.id), page, per_page, 'api.get_histories')
#     return jsonify(data)

# @bp.route('/users', methods=['GET'])
# def get_users():
#     pass
#
#
# @bp.route('/users/<int:id>/followers', methods=['GET'])
# def get_followers(id):
#     pass
#
#
# @bp.route('/users/<int:id>/followed', methods=['GET'])
# def get_followed(id):
#     pass
#
#
# @bp.route('/users', methods=['POST'])
# def create_user():
#     pass
#
#
# @bp.route('/users/<int:id>', methods=['PUT'])
# def update_user(id):
#     pass