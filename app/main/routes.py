from flask import render_template, flash, redirect, url_for, current_app, app, request, Response
from flask_user import current_user, roles_required, user_confirmed_email, login_required

from app.data.models.format import FileFormatModel
from app.data.forms.upload_form import UploadForm
from app.data.forms.company_form import CompanyForm
from app.data.models.user import UserModel
from app.data.models.company import CompanyModel
from app.data.models.history import UploadHistoryModel
from app.data.models.job_log import JobLogModel
from flask_user.forms import RegisterForm, ResendConfirmEmailForm, ForgotPasswordForm, ResetPasswordForm

from app.helpers.validation import validate, check_img_type, save_file, excel_validation, upload_file_to_s3, s3
from app.email import notify_new_user_to_admin, send_password_reset_email, email_confirmation
from app.main import application

from flask_menu import Menu, register_menu
from datetime import datetime

from flask import Flask, request, jsonify, send_file, make_response
# import flask_excel as excel

from app import db
# import boto3

# @user_confirmed_email.connect_via(application)
# def _after_confirmed_hook(sender, user, **extra):
#     notify_new_user_to_admin(user)


@application.route('/welcome')
@login_required
@roles_required('Vendor')
@register_menu(application, '.main', 'Home', order=0)
def welcome():
    user = UserModel.find_by_email(current_user.email)
    return render_template('welcome.html', user=user, title='Welcome')


@application.route('/company', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
@register_menu(application, '.welcome', 'Company Profile', order=3)
def company():
    form = CompanyForm()
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        company_name_duplication = CompanyModel.find_by_name(form.name.data)
        if not form.id.data:
            if company_name_duplication:
                return jsonify({"message": "This company has already registered by other user"}, 400)
            company = CompanyModel(name=form.name.data,
                                   description=form.description.data,
                                   address=form.address.data,
                                   telephone_number=form.telephone_number.data,
                                   toll_free_number=form.toll_free_number.data,
                                   fax_number=form.fax_number.data,
                                   website=form.website.data,
                                   sales_email=form.sales_email.data,
                                   personal_contact_name=form.personal_contact_name.data,
                                   personal_contact_email=form.personal_contact_email.data,
                                   idnumber=form.idnumber.data,
                                   cmpdname=form.cmpdname.data,
                                   cas=form.cas.data,
                                   price=form.price.data,
                                   job_notify_email=form.job_notify_email.data)
            if form.file.data:
                if check_img_type(form.file.data):
                    company.logo = save_file(form.file.data, form.name.data, True)
                else:
                    return False
            company.save_to_db()
            user = UserModel.find_by_email(current_user.email)
            user.company_id = company.id
            user.save_to_db()
        else:
            if company_name_duplication and company_name_duplication.id != int(form.id.data):
                return jsonify({"message": "This company has already registered by other user"}, 400)

            company = CompanyModel.find_by_id(int(form.id.data))
            if form.file.data:
                if check_img_type(form.file.data):
                    if current_app.config["ZINC_MODE"]:
                        company.logo = save_file(form.file.data, "{}_{}".format(current_user.id, form.name.data), True)
                    else:
                        company.logo = upload_file_to_s3(form.file.data, form.name.data, "company-logos")
                else:
                    return False
            company.name = form.name.data
            company.description = form.description.data
            company.address = form.address.data
            company.telephone_number = form.telephone_number.data
            company.toll_free_number = form.toll_free_number.data
            company.fax_number = form.fax_number.data
            company.website = form.website.data
            company.sales_email = form.sales_email.data
            company.personal_contact_name = form.personal_contact_name.data
            company.personal_contact_email = form.personal_contact_email.data
            company.idnumber = form.idnumber.data
            company.cmpdname = form.cmpdname.data
            company.cas = form.cas.data
            company.price = form.price.data
            company.job_notify_email = form.job_notify_email.data
            company.save_to_db()
        flash('Updated!', category='success')
        return jsonify({"message": "Updated!"}, 200)
    elif request.method == 'GET':
        user = UserModel.find_by_email(current_user.email)
        if user.company:
            form.id.data = user.company_id
            form.logo.data = user.company.logo
            form.name.data = user.company.name
            form.description.data = user.company.description
            form.address.data = user.company.address
            form.telephone_number.data = user.company.telephone_number
            form.toll_free_number.data = user.company.toll_free_number
            form.fax_number.data = user.company.fax_number
            form.website.data = user.company.website
            form.sales_email.data = user.company.sales_email
            form.personal_contact_name.data = user.company.personal_contact_name
            form.personal_contact_email.data = user.company.personal_contact_email
            form.idnumber.data = user.company.idnumber
            form.cmpdname.data = user.company.cmpdname
            form.cas.data = user.company.cas
            form.price.data = user.company.price
            form.job_notify_email.data = user.company.job_notify_email
    return render_template('company.html', title='Profile', form=form)


@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        if current_user.has_role('Admin'):
            return redirect(url_for('admin.index'))
        else:
            return redirect(url_for('main.welcome'))
    else:
        return redirect(url_for('user.login'))


@application.route('/help')
@login_required
@roles_required('Vendor')
@register_menu(application, '.fourth', 'Help', order=4)
def help_page():
    return render_template('help.html', title='Help')


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
    return render_template('result.html', title='Job Result', history=history)


@application.route('/result', methods=['GET', 'POST'])
@login_required
def result():
    id = request.args.get('id', type=int)
    history = UploadHistoryModel.find_by_id(id)
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

    return render_template('result.html', title='Job Result', history=history)
    # return render_template('result.html', title='Job Result', history=history, stdout=stdout, stderr=stderr)


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


@application.route('/reset_password_request', methods=['POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.welcome'))
    # form = ResetPasswordRequestForm()
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password', category='success')
        else:
            flash('Your email not registered in our system', category='danger')
        return redirect(url_for('user.login'))
    return render_template('reset_password.html',
                           title='Reset Password', form=form)


@application.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.welcome'))
    user = UserModel.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('user.login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', category='success')
        return redirect(url_for('user.login'))
    return render_template('flask_user/reset_password.html', form=form)


@application.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.welcome'))
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = UserModel(username=register_form.username.data, email=register_form.email.data)
        user.set_password(register_form.password.data)
        user.save_to_db()

        email_confirmation(user)

        flash('Congratulations, you are now a registered user! '
              'A confirmation email has been sent via email.', category='success')
    return render_template('flask_user/login_or_register.html', register_form=register_form, form=register_form, login_form=register_form)


@application.route('/confirm/<token>', methods=['GET'])
def confirm(token):
    try:
        email = UserModel.confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = UserModel.query.filter_by(email=email).first_or_404()
    if user.confirmed_at:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed_at = datetime.now()
        user.save_to_db()
        notify_new_user_to_admin(user)
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.welcome'))


@application.route('/resend_confirmation_email', methods=['POST'])
def resend_confirmation_email():
    form = ResendConfirmEmailForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user:
            email_confirmation(user)
            flash('A confirmation email has been sent via email.', category='success')
        else:
            flash('Your email not registered in our system', category='danger')
    return redirect(url_for('user.login'))


# @application.route('/athena', methods=['GET'])
# def athena():
#     # from pyathenajdbc import connect
#     # conn_str = 'awsathena+jdbc://{}:{}@athena.{}.amazonaws.com:443/{}?s3_staging_dir={}'.format(
#     #     current_app.config['S3_KEY'],
#     #     current_app.config['S3_SECRET'],
#     #     'us-west-2',
#     #     'default',
#     #     's3://aws-athena-query-results-upw/')
#     # conn = connect(conn_str)
#     # try:
#     #     with conn.cursor() as cursor:
#     #         cursor.execute("""
#     #             SELECT * FROM one_row
#     #             """)
#     #         print(cursor.description)
#     #         print(cursor.fetchall())
#     # finally:
#     #     conn.close()
#     res = ""
#     import contextlib
#     from urllib.parse import quote_plus  # PY2: from urllib import quote_plus
#     from sqlalchemy.engine import create_engine
#     from sqlalchemy.sql.expression import select
#     from sqlalchemy.sql.functions import func
#     from sqlalchemy.sql.schema import Table, MetaData
#
#     conn_str = 'awsathena+jdbc://{}:{}@athena.{}.amazonaws.com:443/{}?s3_staging_dir={}'.format(
#         current_app.config['S3_KEY'],
#         current_app.config['S3_SECRET'],
#         'us-west-2',
#         'uploadwizard',
#         's3://aws-athena-query-results-upw/')
#     engine = create_engine(conn_str.format(
#         access_key=quote_plus(current_app.config['S3_KEY']),
#         secret_key=quote_plus(current_app.config['S3_SECRET']),
#         region_name='us-west-2',
#         schema_name='uploadwizard',
#         s3_staging_dir=quote_plus('s3://aws-athena-query-results-upw/')))
#     try:
#         with contextlib.closing(engine.connect()) as conn:
#             many_rows = Table('file', MetaData(bind=engine), autoload=True)
#             rs = select([many_rows.c.manufacturerpartid]).execute()
#             res = ""
#             for row in rs:
#                 res += str(row) +"\n<br/>"
#     finally:
#         engine.dispose()
#     return res

# @app.errorhandler(InvalidUsage)
# def handle_invalid_usage(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response
