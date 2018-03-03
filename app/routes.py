from flask import Blueprint, render_template, flash, redirect, url_for, send_from_directory
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
from app.validation import validate


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(app.static_folder, path)


@app.route('/')
@app.route('/index')
@login_required
def index():
    histories = UploadHistoryModel.find_by_user_id(current_user.id)
    return render_template('index.html', title='Home Page', histories=histories)


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
        flash(validate(form.file.data))
    return render_template('upload.html', title='Upload File', form=form)
