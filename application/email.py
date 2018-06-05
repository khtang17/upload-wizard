from flask_mail import Message
from application import mail
from threading import Thread
from application.data.models.user import UserModel
from flask import render_template, current_app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def notify_new_user_to_admin(user):
    admins = UserModel.get_admins()
    admin_emails = []
    for admin in admins:
        admin_emails.append(admin.email)
    send_email('New user registration!',
               sender=current_app.config['MAIL_DEFAULT_SENDER'],
               recipients=admin_emails,
               text_body=render_template('email/email_confirmation_notify.txt',
                                         user=user),
               html_body=render_template('email/email_confirmation_notify.html',
                                         user=user))


def notify_new_role_to_user(user):
    send_email('You have granted access to system!',
               sender=current_app.config['MAIL_DEFAULT_SENDER'],
               recipients=[user.email],
               text_body=render_template('email/user_role_notify.txt', user=user),
               html_body=render_template('email/user_role_notify.html', user=user))


def notify_job_result_to_user(history):
    send_email('Your job has been finished!',
               sender=current_app.config['MAIL_DEFAULT_SENDER'],
               recipients=[history.user.email],
               text_body=render_template('email/job_result_notify.txt', history=history),
               html_body=render_template('email/job_result_notify.html', history=history))
