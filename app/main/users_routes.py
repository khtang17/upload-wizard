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
from app.helpers import *
from app.email import notify_new_user_to_admin, send_password_reset_email, email_confirmation
from app.main import application

from flask_menu import Menu, register_menu
from datetime import datetime

from flask import Flask, request, jsonify, send_file, make_response
# import flask_excel as excel

from app import db


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
        return redirect(url_for('user.login'))
    user = UserModel.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('user.login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
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
        # return jsonify({"message": "Updated!"}, 200)
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
