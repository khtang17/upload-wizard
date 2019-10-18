from flask import app
import json, os
from flask import render_template, url_for, current_app
from flask_login import current_user
from sqlalchemy import extract
from app.data.models.history import UploadHistoryModel
import codecs
import logging
from datetime import datetime


# example_folder = os.path.join(app.instance_path, 'static/catalog_examples')

ZINC_CATALOG_LIST = "/nfs/home/khtang/code/upload_wizard_codes/catalog_shortname.txt"
def get_catalog_shortname():
    file_name = 'JOB_INFO.txt'
    try:
        with open(file_name, 'r') as fh:
            job_info = json.load(fh)
    except IOError as e:
        logging.error("Unable to open {0}:  ".format(file_name) + e)
    short_name = job_info['short_name']
    # catalog_type = job_info['catalog_type']
    # availability = job_info['availability']

    # short_name = ''
    # if catalog_type == 'both' or catalog_type == 'sc':
    #     short_name = company_basename
    # else:
    #     short_name = company_basename + catalog_type
    # if availability == 'demand':
    #     short_name = short_name + '-v'
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
    return user_job_count

def get_shortname_list():
    with open(ZINC_CATALOG_LIST, 'r') as catalog_file:
        catalogs = catalog_file.readlines()
        catalog_file.close()
    shortname_list = []
    for catalog in catalogs:
        shortname_list.append(catalog.strip('\n'))
    return shortname_list