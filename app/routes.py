from flask import render_template, flash, redirect, url_for, Blueprint
from app import app
from flask_user import current_user, roles_required, user_confirmed_email

from app.data.models.format import FileFormatModel
from app.data.forms.upload_form import UploadForm
from app.data.forms.company_form import CompanyForm
from app.data.models.user import UserModel
from app.data.models.company import CompanyModel
from flask import request
# from werkzeug.urls import url_parse

from app.exception import InvalidUsage
from app.helpers.validation import validate

from flask import jsonify
from flask_user import login_required

from app.email import notify_new_user_to_admin

# user_blueprint = Blueprint('user_blueprint', __name__, static_folder='/static')


@user_confirmed_email.connect_via(app)
def _after_confirmed_hook(sender, user, **extra):
    notify_new_user_to_admin(user)


# @user_logged_in.connect_via(app)
# def _after_login_hook(sender, user, **extra):
#     sender.logger.info('user logged in')

@app.route('/company', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
def company():
    form = CompanyForm()
    if form.validate_on_submit():
        company_name_duplication = CompanyModel.find_by_name(form.name.data)
        if not form.id.data:
            if company_name_duplication:
                flash('This company has already registered by other user', category="danger")
                return redirect(url_for('company'))
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
            company.save_to_db()
            user = UserModel.find_by_email(current_user.email)
            user.company_id = company.id
            user.save_to_db()
        else:
            if company_name_duplication and company_name_duplication.id != int(form.id.data):
                flash('This company has already registered by other user', category="danger")
                return redirect(url_for('company'))
            company = CompanyModel.find_by_id(int(form.id.data))
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
            print(company.personal_contact_email)
            print(form.personal_contact_email.data)
            company.idnumber = form.idnumber.data
            company.cmpdname = form.cmpdname.data
            company.cas = form.cas.data
            company.price = form.price.data
            company.save_to_db()
        flash('Updated!', category="success")
        return redirect(url_for('company'))
    elif request.method == 'GET':
        user = UserModel.find_by_email(current_user.email)
        if user.company:
            form.id.data = user.company_id
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


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_anonymous:
        return redirect(url_for('user.login'))
    elif current_user.has_role('Admin'):
        return redirect(url_for('admin.index'))
    elif current_user.has_role('Vendor'):
        return redirect(url_for('history'))
    else:
        return redirect(url_for('welcome'))


@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html', title='Welcome')


@app.route('/help')
@login_required
def help_page():
    return render_template('help.html', title='Help')


@app.route('/history', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
def history():
    page = request.args.get('page', 1, type=int)
    histories = current_user.upload_histories.paginate(
        page, app.config['LISTS_PER_PAGE'], False)
    next_url = url_for('history', page=histories.next_num) \
        if histories.has_next else None
    prev_url = url_for('history', page=histories.prev_num) \
        if histories.has_prev else None
    pagestart = (page-1)*app.config['LISTS_PER_PAGE']
    return render_template('history.html', title='Home Page', histories=histories.items,
                           next_url=next_url,
                           prev_url=prev_url,
                           pagestart=pagestart)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
def upload():
    # file_format = FileFormatModel(title='smiles', col_type="str", order=1)
    # file_format.save_to_db()
    # file_format = FileFormatModel(title='product_id', col_type="str", order=2)
    # file_format.save_to_db()
    # file_format = FileFormatModel(title='cas_number', col_type="str", order=3)
    # file_format.save_to_db()
    form = UploadForm()
    formats = FileFormatModel.find_all()
    if form.validate_on_submit():
        return_msg = validate(form.file.data, form)
        print(return_msg[0]['message'])
        print(return_msg[1])
        return jsonify(return_msg)
    return render_template('upload.html', title='Upload File', form=form, formats=formats)


# @app.errorhandler(InvalidUsage)
# def handle_invalid_usage(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response


# @app.route('/admin/', methods=['GET', 'POST'])
# @login_required
# @roles_required('Admin')    # Use of @roles_required decorator
# def admin_page():
#     return render_template('admin/index.html', title='Upload File')
