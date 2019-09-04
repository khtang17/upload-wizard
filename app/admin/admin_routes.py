from flask import render_template, flash, redirect, url_for, current_app, app, request, Response
from flask_user import current_user, roles_required, user_confirmed_email, login_required
from app.constants import *
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
from app.admin import admin_blueprint
from datetime import datetime
from flask_menu import Menu, register_menu
from datetime import datetime, timezone
from datetime import date
import pdb
from pdb import set_trace

from .admin_help import get_job_status_count




@admin_blueprint.route('/upload_report', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def upload_report():
    this_month = date.today().strftime("%B - %Y")
    histories = UploadHistoryModel.query.order_by(UploadHistoryModel.status_id.desc())
    status_count, job_count = get_job_status_count()
    return render_template('admin/report.html', title='Report Page', histories=histories,
                            JOB_STATUS=JOB_STATUS, CATALOG_TYPE=CATALOG_TYPE, this_month=this_month, job_count=job_count, status_count=status_count)

# @application.route('/admin_cronjob', methods=['GET', 'POST'])
# @login_required
# @roles_required('Admin')
# def cronjob():
#     pass




