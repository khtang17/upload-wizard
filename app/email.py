from flask_mail import Message
from app import app, mail
from threading import Thread
from app.data.models.user import UserModel
from flask import render_template


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def notify_new_user_to_admin(user):
    admins = UserModel.get_admins()
    admin_emails = []
    for admin in admins:
        admin_emails.append(admin.email)
    send_email('New user registration!',
               sender=app.config['MAIL_DEFAULT_SENDER'],
               recipients=admin_emails,
               text_body=render_template('email/email_confirmation_notify.txt',
                                         user=user),
               html_body=render_template('email/email_confirmation_notify.html',
                                         user=user))
