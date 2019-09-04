from flask import app
import json, os
from flask import render_template, url_for, current_app
from flask_login import current_user
from sqlalchemy import extract
from app.data.models.history import UploadHistoryModel
import codecs
from datetime import datetime


# example_folder = os.path.join(app.instance_path, 'static/catalog_examples')


def get_catalog_shortname():
    file_name = 'JOB_INFO.txt'
    try:
        with open(file_name, 'r') as fh:
            job_info = json.load(fh)
    except IOError:
        pass
    company_basename = job_info['company_basename']
    catalog_type = job_info['catalog_type']
    availability = job_info['availability']

    short_name = ''
    if catalog_type == 'both' or catalog_type == 'sc':
        short_name = company_basename
    else:
        short_name = company_basename + catalog_type
    if availability == 'demand':
        short_name = short_name + '-v'
    return short_name


def print_on_browser(file_type):
    example_folder = os.path.join(current_app.config['STATIC_FOLDER'], 'catalog_examples')
    example_list = os.listdir(example_folder)
    display = ''
    for file in example_list:
        if file_type in file:
            display = file
    file_path = os.path.join(example_folder, display)
    with codecs.open(file_path, 'r', encoding='utf-8', errors='ignore') as file_reader:
        file_content = file_reader.readlines()
        file_reader.close()
    return render_template('example.html', file_content=file_content)

def get_user_job_count():
    monthly_user_upload_job = UploadHistoryModel.get_this_month_upload()
    user_job_count = len(monthly_user_upload_job)
    if user_job_count is None:
        user_job_count = 0
    #user_job_count = UploadHistoryModel.query.filter(extract('month', UploadHistoryModel.date_uploaded) == this_month).all()
    return user_job_count