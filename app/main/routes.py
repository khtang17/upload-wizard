from flask import render_template, flash, redirect, url_for, current_app, app
from flask_user import current_user, roles_required, user_confirmed_email, login_required

from app.data.models.format import FileFormatModel
from app.data.forms.upload_form import UploadForm
from app.data.forms.company_form import CompanyForm
from app.data.models.user import UserModel
from app.data.models.company import CompanyModel
from app.data.models.history import UploadHistoryModel
from app.data.models.job_log import JobLogModel
from flask import request

from app.helpers.validation import validate, check_img_type, save_file, allowed_file2, excel_validation
from app.email import notify_new_user_to_admin
from app.main import bp
import os

from flask import Flask, request, jsonify
import flask_excel as excel


@user_confirmed_email.connect_via(bp)
def _after_confirmed_hook(sender, user, **extra):
    notify_new_user_to_admin(user)


@bp.route('/welcome')
@login_required
# @menu.register_menu(app, '.', 'Home')
def welcome():
    user = UserModel.find_by_email(current_user.email)
    return render_template('welcome.html', user=user, title='Welcome')


@bp.route('/company', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
# @menu.register_menu(app, '.third', 'Company', order=3)
def company():
    form = CompanyForm()
    print(form.validate_on_submit())
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
                                   price=form.price.data)

            if form.file.data:
                if check_img_type(form.file.data):
                    company.logo = save_file(form.file.data, form.name.data, True)
                    print(company.logo)
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
                    company.logo = save_file(form.file.data, form.name.data, True)
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
    return render_template('company.html', title='Profile', form=form)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        if current_user.has_role('Admin'):
            return redirect(url_for('admin.index'))
        else:
            return redirect(url_for('main.welcome'))
    else:
        return redirect(url_for('user.login'))


@bp.route('/help')
@login_required
# @menu.register_menu(app, '.fourth', 'Help', order=4)
def help_page():
    return render_template('help.html', title='Help')


@bp.route('/history', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
# @menu.register_menu(app, '.first', 'History', order=1)
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


@bp.route('/result', methods=['GET', 'POST'])
@login_required
def result():
    id = request.args.get('id', type=int)
    history = UploadHistoryModel.find_by_id(id)
    if history.user.id != current_user.id:
        return render_template('errors/404.html'), 404
    stdout = ""
    stderr = ""
    process = ""
    base_folder = current_app.config['UPLOAD_FOLDER']
    folder = "{}/{}_vendor/{}/".format(base_folder, current_user.id, id)
    if not os.path.exists(os.path.realpath(os.path.dirname(folder))):
        folder = "{}/{}_{}/{}/".format(base_folder, current_user.id, current_user.short_name, id)
    file_dir = os.path.realpath(os.path.dirname(folder))
    print(file_dir)
    print(os.path.join(file_dir, "stdout"))
    if os.path.isfile(os.path.join(file_dir, "stdout")):
        with open(os.path.join(file_dir, "stdout"), 'r') as file1:
            stdout = file1.read()
            file1.close()
        with open(os.path.join(file_dir, "stderr"), 'r') as file2:
            stderr = file2.read()
            stderr = stderr.replace("%", "")
            stderr = stderr.replace('\n', "<br/>")
            file2.close()
    else:
        process = "Job process is not finished yet!"

    return render_template('result.html', title='Job Result', history=history, process=process,
                           stdout=stdout,
                           stderr=stderr)
    # return render_template('result.html', title='Job Result', history=history)


@bp.route('/job_logs', methods=['GET'])
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


@bp.route('/upload', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
# @menu.register_menu(app, '.second', 'Upload', order=2)
def upload():
    form = UploadForm()
    formats = FileFormatModel.find_all()
    if request.method == 'POST' and form.validate_on_submit():
        if allowed_file2(form.file.data.filename):
            #return jsonify({"result": request.get_book_dict(field_name='file')})
            excel_validation(request)
        return_msg = validate(form.file.data, form)
        return jsonify(return_msg)
    return render_template('upload.html', title='Upload File', form=form, formats=formats)


@bp.route('/histories', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
def get_histories():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    data = UploadHistoryModel.to_all_collection_dict(
        UploadHistoryModel.query.filter_by(user_id=current_user.id), page, per_page, 'ID')
    return jsonify(data)


@bp.route("/upload2", methods=['GET', 'POST'])
def upload_file2():
    if request.method == 'POST':
        return jsonify({"result": request.get_book_dict(field_name='file')})
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    '''

# @app.errorhandler(InvalidUsage)
# def handle_invalid_usage(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response