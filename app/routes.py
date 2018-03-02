from flask import render_template, flash, redirect, url_for
from app import app
from flask_login import current_user, login_user, login_required
from flask_login import logout_user
from app.data.models.user import User
from app import db
from app.data.forms.login_form import LoginForm
from app.data.forms.registration_form import RegistrationForm
from app.data.forms.upload_form import UploadForm
from flask import request
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Chinzo'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in San Francisco!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home Page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('user/register.html', title='Register', form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        file = form.file.data
        lineNumber = 0
        for line in file.stream:
            lineNumber += 1
            cols = line.decode().strip().split('\t')
            print(line)
            print(cols[0])
            if len(cols) >= 2 and isinstance(cols[0], int) and isinstance(cols[1], str):
                flash('Invalid username or password')
                return redirect(url_for('upload'))
        # form.file.data.save('uploads/' + filename)
        return redirect(url_for('upload'))

    return render_template('upload.html', title='Upload File', form=form)
