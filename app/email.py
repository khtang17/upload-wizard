from flask_mail import Message
from app import mail
from threading import Thread
from app.data.models.user import UserModel
from flask import render_template, current_app

import boto3
from botocore.exceptions import ClientError

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "upload.vendor@gmail.com"

# Replace recipient@example.com with a "To" address. If your account
# is still in the sandbox, this address must be verified.
RECIPIENT = "chinzo.dandar@gmail.com"

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the
# ConfigurationSetName=CONFIGURATION_SET argument below.
# CONFIGURATION_SET = "ConfigSet"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-west-2"


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body, sync=False):
    # msg = Message(subject, sender=sender, recipients=recipients)
    # msg.body = text_body
    # msg.html = html_body
    # if sync:
    #     mail.send(msg)
    # else:
    #     Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': recipients,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': html_body,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': text_body,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=sender,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Upload Wizard] Reset Your Password',
               sender=current_app.config['MAIL_DEFAULT_SENDER'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


def notify_new_user_to_admin(user):
    admins = UserModel.get_admins()
    admin_emails = []
    for admin in admins:
        admin_emails.append(admin.email)
    send_email('New user registration!',
               sender=current_app.config['MAIL_DEFAULT_SENDER'],
               recipients=admin_emails,
               text_body=render_template('email/email_confirmation_notify.txt', user=user),
               html_body=render_template('email/email_confirmation_notify.html', user=user))


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
