from flask import render_template, flash, redirect, url_for
from app import app
from flask_login import current_user, login_user, login_required
from flask_login import logout_user

from app.data.models.history import UploadHistoryModel
from app.data.models.user import UserModel
from app.data.models.company import CompanyModel
from app.data.forms.login_form import LoginForm
from app.data.forms.registration_form import RegistrationForm
from app.data.forms.upload_form import UploadForm
from flask import request
from werkzeug.urls import url_parse

from app.exception import InvalidUsage
from app.helpers.validation import validate
from flask import send_from_directory

from flask import jsonify

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.instance_path, filename)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    histories = current_user.upload_histories.paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=histories.next_num) \
        if histories.has_next else None
    prev_url = url_for('index', page=histories.prev_num) \
        if histories.has_prev else None
    pagestart = (page-1)*app.config['POSTS_PER_PAGE']
    return render_template('index.html', title='Home Page', histories=histories.items,
                           next_url=next_url,
                           prev_url=prev_url,
                           pagestart=pagestart)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.find_by_email(form.email.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('user/login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        company = CompanyModel.find_by_name(form.company_name.data)
        if not company:
            company = CompanyModel(name=form.company_name.data)
            company.save_to_db()
        user = UserModel(username=form.username.data, email=form.email.data, company_id=company.id)
        user.set_password(form.password.data)
        user.save_to_db()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('user/register.html', title='Register', form=form)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        print('validated')
        flash(validate(form.file.data))
        raise InvalidUsage('File uploaded', status_code=200)
    return render_template('upload.html', title='Upload File', form=form)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
