from flask import render_template, flash, redirect, url_for, current_app, app, request, Response
from flask_user import current_user, roles_required, user_confirmed_email, login_required
from app.constants import JOB_STATUS, CATALOG_TYPE

from app.data.models.user import UserModel
from app.data.models.history import UploadHistoryModel
from app.main import application


from flask_menu import Menu, register_menu
from datetime import datetime

from flask import Flask, request, jsonify, send_file, make_response
# import flask_excel as excel

from app import db
# import boto3

# @user_confirmed_email.connect_via(application)
# def _after_confirmed_hook(sender, user, **extra):
#     notify_new_user_to_admin(user)
@application.route('/')
@application.route('/home')
def home():
    return render_template('home.html', title='Home Page')


@application.route('/welcome')
@login_required
@register_menu(application, '.main', 'Home', order=0)
def welcome():
    user = UserModel.find_by_email(current_user.email)
    latest_history = UploadHistoryModel.get_last_by_user_id(user_id=user.id)
    if latest_history:
        catalog_type = CATALOG_TYPE.get(latest_history.catalog_type)
        status = JOB_STATUS.get(latest_history.status_id)
        return render_template('welcome.html', user=user, title='Welcome', latest_history=latest_history, catalog_type=catalog_type, status=status)
    else:
        return render_template('welcome.html', user=user, title='Welcome')



# @application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        if current_user.has_role('Admin'):
            return redirect(url_for('admin_views.upload_report'))
        else:
            return redirect(url_for('main.welcome'))
    else:
        return redirect(url_for('user.login'))


@application.route('/help')
@register_menu(application, '.fourth', 'Help', order=4)
def help_page():
    return render_template('help.html', title='Help')





@application.route('/athena', methods=['GET'])
def athena():
    # from pyathenajdbc import connect
    # conn_str = 'awsathena+jdbc://{}:{}@athena.{}.amazonaws.com:443/{}?s3_staging_dir={}'.format(
    #     current_app.config['S3_KEY'],
    #     current_app.config['S3_SECRET'],
    #     'us-west-2',
    #     'default',
    #     's3://aws-athena-query-results-upw/')
    # conn = connect(conn_str)
    # try:
    #     with conn.cursor() as cursor:
    #         cursor.execute("""
    #             SELECT * FROM one_row
    #             """)
    #         print(cursor.description)
    #         print(cursor.fetchall())
    # finally:
    #     conn.close()
    res = ""
    import contextlib
    from urllib.parse import quote_plus  # PY2: from urllib import quote_plus
    from sqlalchemy.engine import create_engine
    from sqlalchemy.sql.expression import select
    from sqlalchemy.sql.functions import func
    from sqlalchemy.sql.schema import Table, MetaData

    conn_str = 'awsathena+jdbc://{}:{}@athena.{}.amazonaws.com:443/{}?s3_staging_dir={}'.format(
        current_app.config['S3_KEY'],
        current_app.config['S3_SECRET'],
        'us-west-2',
        'uploadwizard',
        's3://aws-athena-query-results-upw/')
    engine = create_engine(conn_str.format(
        access_key=quote_plus(current_app.config['S3_KEY']),
        secret_key=quote_plus(current_app.config['S3_SECRET']),
        region_name='us-west-2',
        schema_name='uploadwizard',
        s3_staging_dir=quote_plus('s3://aws-athena-query-results-upw/')))
    try:
        with contextlib.closing(engine.connect()) as conn:
            many_rows = Table('file', MetaData(bind=engine), autoload=True)
            rs = select([many_rows.c.manufacturerpartid]).execute()
            res = ""
            for row in rs:
                res += str(row) +"\n<br/>"
    finally:
        engine.dispose()
    return res

# @app.errorhandler(InvalidUsage)
# def handle_invalid_usage(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response
