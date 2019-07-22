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
from app.email import notify_new_user_to_admin, send_password_reset_email, email_confirmation
from app.admin import application
from datetime import datetime
from flask_menu import Menu, register_menu
from datetime import datetime, timezone

from flask import Flask, request, jsonify, send_file, make_response
# import flask_excel as excel


@application.route('/load2d_report')
@login_required
@roles_required('Admin')
def load2d_report():
    page = request.args.get("page", 1, type=int)
    histories = UploadHistoryModel.query.order_by(UploadHistoryModel.status_id.desc()).paginate(
        page, current_app.config['LISTS_PER_PAGE'], False)
    # histories = current_user.upload_histories.paginate(
    #     page, current_app.config['LISTS_PER_PAGE'], False)
    next_url = url_for('admin_views.load2d_report', page=histories.next_num) \
        if histories.has_next else None
    prev_url = url_for('admin_views.load2d_report', page=histories.prev_num) \
        if histories.has_prev else None
    pagestart = (page - 1) * current_app.config['LISTS_PER_PAGE']
    return render_template('history.html', title='Report Page', histories=histories.items,
                           next_url=next_url,
                           prev_url=prev_url,
                           pagestart=pagestart)


