from flask import render_template, flash, redirect, url_for, current_app, app, request, Response
from flask_user import current_user, roles_required, user_confirmed_email, login_required

from app.data.models.format import FileFormatModel
from app.data.forms.upload_form import UploadForm
from app.data.forms.company_form import CompanyForm
from app.data.models.user import UserModel
from app.data.models.company import CompanyModel
from app.data.models.history import UploadHistoryModel
from app.data.models.job_log import JobLogModel
from app.data.models.status import StatusModel
from flask_user.forms import RegisterForm, ResendConfirmEmailForm, ForgotPasswordForm, ResetPasswordForm

# from app.helpers.validation import validate, check_img_type, save_file, excel_validation, upload_file_to_s3, s3
from app.helpers.validation import validate, excel_validation, s3
from app.email import notify_new_user_to_admin, send_password_reset_email, email_confirmation
from app.main import application

from flask_menu import Menu, register_menu
from datetime import datetime, timezone

from flask import Flask, request, jsonify, send_file, make_response
# import flask_excel as excel



@application.route('/history', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
@register_menu(application, '.first', 'History', order=1)
def history():
    page = request.args.get('page', 1, type=int)
    histories = current_user.upload_histories.paginate(
        page, current_app.config['LISTS_PER_PAGE'], False)
    next_url = url_for('main.history', page=histories.next_num) \
        if histories.has_next else None
    prev_url = url_for('main.history', page=histories.prev_num) \
        if histories.has_prev else None
    pagestart = (page-1)*current_app.config['LISTS_PER_PAGE']
    return render_template('history.html', title='Home Page', histories=histories.items,
                           next_url=next_url,
                           prev_url=prev_url,
                           pagestart=pagestart)


@application.route('/last_result', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
def last_result():
    history = UploadHistoryModel.get_last_by_user_id(current_user.id)
    last_updated = history.last_updated

    status = StatusModel.query.filter_by(status_id=history.status_id).first()
    statuses_dict = StatusModel.to_dict()
    return render_template('result.html', title='Job Result', history=history, status=status.status, last_updated=last_updated, statuses_dict=statuses_dict, status_id = status.status_id)

@application.route('/get_status_update', methods =['GET', 'POST'])
@login_required
def get_status_update():
    history_id = request.args.get('history_id', type=int)
    history = UploadHistoryModel.query.filter_by(id=history_id)
    status = StatusModel.query.filter_by(status_id = history.status_id)
    print(status)
    return jsonify({'status_id': status})


@application.route('/result', methods=['GET', 'POST'])
@login_required
def result():
    id = request.args.get('id', type=int)
    history = UploadHistoryModel.find_by_id(id)
    last_updated = history.last_updated
    statuses_dict = StatusModel.to_dict()
    status = StatusModel.query.filter_by(status_id=history.status_id).first()
    if history.user.id != current_user.id and current_user.has_role('Vendor'):
        return render_template('errors/404.html'), 404
    # stdout = ""
    # stderr = ""
    # base_folder = current_app.config['UPLOAD_FOLDER']
    # folder = "{}/{}_vendor/{}/".format(base_folder, current_user.id, id)
    # if not os.path.exists(os.path.realpath(os.path.dirname(folder))):
    #     folder = "{}/{}_{}/{}/".format(base_folder, current_user.id, current_user.short_name, id)
    # file_dir = os.path.realpath(os.path.dirname(folder))
    # print(file_dir)
    # print(os.path.join(file_dir, "stdout"))
    # if os.path.isfile(os.path.join(file_dir, "stdout")):
    #     with open(os.path.join(file_dir, "stdout"), 'r') as file1:
    #         stdout = file1.read()
    #         file1.close()
    #     with open(os.path.join(file_dir, "stderr"), 'r') as file2:
    #         stderr = file2.read()
    #         stderr = stderr.replace("%", "")
    #         stderr = stderr.replace('\n', "<br/>")
    #         file2.close()

    return render_template('result.html', title='Job Result', history=history, status=status.status, last_updated=last_updated, statuses_dict=statuses_dict, status_id = status.status_id)
    # return render_template('result.html', title='Job Result', history=history, stdout=stdout, stderr=stderr)

#
# @application.route('/catalog_resutls', methods=['POST'])
# @login_required
# def catalog_results():
#     history_id = request.args.get('history_id', type=int)
#     return_msg = gather_info(history_id)
#     return return_msg


@application.route('/job_logs', methods=['GET'])
@login_required
def job_logs():
    history_id = request.args.get('history_id', type=int)
    id = request.args.get('id', type=int)
    job_logs = JobLogModel.find_by_history(history_id, id)
    return jsonify([{
        'id': l.id,
        'status': l.status,
        'status_type': l.status_type,
        'date': l.date
    } for l in job_logs])


@application.route('/upload', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
@register_menu(application, '.second', 'File Upload', order=2)
def upload():
    if current_app.config['ZINC_MODE']:
        form = UploadForm()
        formats = FileFormatModel.find_all()
        if request.method == 'POST' and form.validate_on_submit():
            return_msg = validate(form.file.data, form)
            return jsonify(return_msg)
        # else:
        #     # return_msg = validate(form)
        #     return jsonify(return_msg)
        return render_template('upload.html', title='Upload File', form=form, formats=formats)
    else:
        if request.method == 'POST':
            return jsonify(excel_validation(request))
        return render_template('upload.html', title='Upload File')


@application.route('/histories', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
def get_histories():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    data = UploadHistoryModel.to_all_collection_dict(
        UploadHistoryModel.query.filter_by(user_id=current_user.id).order_by(
            UploadHistoryModel.id.desc()), page, per_page, 'ID')
    return jsonify(data)


@application.route("/export/<history_id>/<status_id>", methods=['GET'])
@login_required
def export(history_id, status_id):
    history = UploadHistoryModel.find_by_id(history_id)
    if history.user.id != current_user.id and current_user.has_role('Vendor'):
        return render_template('errors/404.html'), 404

    # 1 - Validated
    # 2 - Validation-err
    # 3 - Unvalidated
    status = ""

    if status_id.startswith('1'):
        status = 'validated'
    elif status_id.startswith('2'):
        status = 'validation-error'
    elif status_id.startswith('3'):
        status = 'unvalidated'

    file = s3.get_object(Bucket=current_app.config['S3_BUCKET'], Key='{}/{}.csv'.format(status, history_id))

    return Response(
        file['Body'].read(),
        mimetype='application/csv',
        headers={"Content-Disposition": "attachment;filename=export_raw_data_{}.csv".format(history_id)}
    )

