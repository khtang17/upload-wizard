from app.api import bp
from app.data.models.job_log import JobLogModel
from app.data.models.history import UploadHistoryModel
from flask import request, jsonify
from app.api.auth import token_auth
from app.api.errors import bad_request
from flask import g


@bp.route('/job_logs', methods=['POST'])
@token_auth.login_required
def create_log():
    data = request.get_json() or {}
    print(data)
    if 'history_id' not in data or 'status' not in data or 'status_type' not in data:
        return bad_request('must include id, status and status_type fields')
    if UploadHistoryModel.query.filter_by(id=data['history_id'], user_id=g.current_user.id).first() is None:
        return bad_request('please check history_id')
    job_log = JobLogModel()
    job_log.from_dict(data)
    job_log.save_to_db()
    response = jsonify(job_log.to_dict())
    response.status_code = 201
    return response
