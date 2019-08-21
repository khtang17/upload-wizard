from flask import app
import json, os
from flask import render_template, url_for, current_app

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
    with open(file_path, 'r') as file_reader:
        file_content = file_reader.readlines()
        file_reader.close()
    return render_template('example.html', file_content=file_content)