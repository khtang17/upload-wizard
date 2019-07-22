from app.api import application
from app import db
from app.data.models.job_log import JobLogModel
from flask_user import current_user
from flask_login import current_user, login_required
from app.data.models.history import UploadHistoryModel
from app.data.models.status import StatusModel
from app.data.models.catalog_info import CatalogResultInfo
from flask import request, jsonify
from app.api.auth import token_auth
from app.api.errors import bad_request
from flask import g
from app.helpers.catalog_result import get_results



@application.route('/update_job_status', methods=['PUT'])
@token_auth.login_required
def update_job_status():
    data = request.get_json() or {}
    if 'history_id' not in data or 'status_id' not in data:
        return bad_request('must include id and status_id fields')
    history = UploadHistoryModel.query.filter_by(id=data['history_id'], user_id=g.current_user.id).first()
    if history is None:
        return bad_request('please check history_id')
    new_status = data['status_id']
    history.modify_status(new_status=new_status)
    response = jsonify(history.to_dict())
    response.status_code = 201
    return response

@application.route('/_get_current_status', methods=['GET'])
@login_required
def get_current_status():
    history_id = request.args.get('history_id', type=int)
    current = UploadHistoryModel.query.filter_by(id=history_id).first()
    last_updated = current.last_updated
    date = last_updated.strftime("%B %d, %Y %I:%M %p")
    status = StatusModel.query.filter_by(status_id=current.status_id).first()
    return jsonify({'status' : status.status,
                    'last_updated': date})

@application.route('/_get_catalog_results', methods=['GET'])
@login_required
def get_catalog_results():
    history_id = request.args.get('history_id', type=int)
    data = get_results(history_id)
    return data

#
@application.route('/_write_job_results', methods=['POST'])
@token_auth.login_required
def write_job_result():
    data = request.get_json() or {}
    print(data)
    if 'history_id' not in data or 'size' not in data or 'filtered' not in data or 'errors' not in data:
        return bad_request('must include history_id, size, filtered and errors fields')
    if UploadHistoryModel.query.filter_by(id=data['history_id'], user_id=g.current_user.id).first() is None:
        return bad_request('please check history_id')
    result = CatalogResultInfo()
    result.from_dict(data)
    result.save_to_db()
    response = jsonify(result.to_dict())
    response.status_code = 201
    return response


