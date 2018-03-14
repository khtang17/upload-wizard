from flask import render_template, flash, redirect, url_for
from app import app, db
# from flask_security import login_user, login_required, roles_required, logout_user
from flask_user import current_user, roles_required

from app.data.models.format import FileFormatModel
from app.data.models.history import UploadHistoryModel
from app.data.models.user import UserModel
from app.data.models.company import CompanyModel
from app.data.forms.login_form import LoginForm
from app.data.forms.registration_form import RegistrationForm
from app.data.forms.upload_form import UploadForm
from flask import request
# from werkzeug.urls import url_parse
#
from app.exception import InvalidUsage
from app.helpers.validation import validate
# from flask import send_from_directory

from flask import jsonify

from flask_user import login_required

# from flask_user import current_user, login_required, roles_required

#
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.instance_path, filename)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = UserModel.find_by_email(form.email.data)
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid email or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('index')
#         return redirect(next_page)
#     return render_template('user/login.html', title='Sign In', form=form)
#
#
# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         company = CompanyModel.find_by_name(form.company_name.data)
#         if not company:
#             company = CompanyModel(name=form.company_name.data,
#                                    description=form.company_description.data,
#                                    address=form.company_address.data,
#                                    telephone_number=form.company_telephone_number.data,
#                                    toll_free_number=form.company_toll_free_number.data,
#                                    fax_number=form.company_fax_number.data,
#                                    website=form.company_website.data,
#                                    sales_email=form.company_email.data)
#             company.save_to_db()
#         user = UserModel(username=form.username.data, email=form.email.data, company_id=company.id)
#         user.set_password(form.password.data)
#         user.save_to_db()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('login'))
#     return render_template('user/register.html', title='Register', form=form)

@app.route('/profile')
@login_required
@roles_required('Vendor')
def profile():
    return '<h1>This is the protected profile page!</h1>'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return '<h1>Welcome</h1>'


@app.route('/history', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
def history():
    page = request.args.get('page', 1, type=int)
    histories = current_user.upload_histories.paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('history', page=histories.next_num) \
        if histories.has_next else None
    prev_url = url_for('history', page=histories.prev_num) \
        if histories.has_prev else None
    pagestart = (page-1)*app.config['POSTS_PER_PAGE']
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
        return_msg = validate(form.file.data)
        print(form.file)
        #flash(validate(form.file.data))
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
