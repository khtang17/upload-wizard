from flask import current_app, jsonify
import os, sys
import shlex
import subprocess
from flask_user import current_user
from app.helpers.upload_tools import get_catalog_shortname
#

# def gather_info():
#     user_folder = str(current_user.id) + "_" + current_user.short_name
#     folder = os.path.join(current_app.config("UPLOAD_FOLDER"), user_folder)
#     print(folder)
#     if folder is None:
#         pass
#     else:
#         os.chdir(folder)
#         short_name = get_catalog_shortname()
#         load_dir = os.path.join(folder, short_name)
#         os.chdir(load_dir)
#         list_process = subprocess.Popen(['wc', '-l', 'list'], stdout=subprocess.PIPE)
#         list = list_process.communicate()[0]
#         list = list.decode('UTF-8').split(' ')[0]
#         filtered_process = subprocess.Popen(['wc', '-l', 'filtered'], stdout=subprocess.PIPE)
#         filtered = filtered_process.communicate()[0]
#         filtered = filtered.decode('UTF-8').split(' ')[0]
#         errors_process = subprocess.Popen(['wc', '-l', 'errors'], stdout=subprocess.PIPE)
#         errors = errors_process.communicate()[0]
#         errors = errors.decode('UTF-8').split(' ')[0]
#         return list, filtered, errors
#


def write_results_to_table(history_id):
    data = get_results(history_id)
    user_token = current_user.get_token()
    try:
        cmd = '''curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{}' -H "Authorization: Bearer {}" gimel.compbio.ucsf.edu:5020/api/_write_job_results'''.format(data, user_token)
        curl_cmd= shlex.split(cmd)
        os.system(curl_cmd)
        return {"message": "Curl cmd success!"}, 200
    except Exception as e:
        return {"message": "Curl cmd Failed"}, 400


def get_results(history_id):
    user_folder = str(current_user.id) + "_" +current_user.short_name+"/"+str(history_id)
    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], user_folder)
    os.chdir(folder)
    short_name = get_catalog_shortname()
    load_result = folder +"/" + short_name +"/" + "RESULTS.txt"

    with open(load_result, 'r') as fh:
        tmp = fh.readlines()
        fh.close()
    data_list = []
    for item in tmp:
        item = item.strip('\n').split(":")[1]
        data_list.append(item)
    data  = jsonify({ 'history_id' : history_id,
                      'size' : data_list[0],
                      'filtered': data_list[1],
                      'errors': data_list[2]
                    })
    return data