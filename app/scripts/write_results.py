#!/usr/bin/env python
# -*- tab-width:4;indent-tabs-mode:f;show-trailing-whitespace:t;rm-trailing-spaces:t -*-
# vi: set ts=4 et sw=4:

import os, sys
from flask import jsonify
import subprocess
from flask_user import current_user
import shlex
cmd = "python write_results.py <dir>"
def gather_and_sort():

    pass

def main():
    folder = sys.argv[1]
    history_id = sys.argv[2]
    os.chdir(folder)
    list_process = subprocess.Popen(['wc', '-l', 'list'], stdout=subprocess.PIPE)
    list = list_process.communicate()[0]
    list = list.decode('UTF-8').split(' ')[0]
    filtered_process = subprocess.Popen(['wc', '-l', 'filtered'], stdout=subprocess.PIPE)
    filtered = filtered_process.communicate()[0]
    filtered = filtered.decode('UTF-8').split(' ')[0]
    errors_process = subprocess.Popen(['wc', '-l', 'errors'], stdout=subprocess.PIPE)
    errors = errors_process.communicate()[0]
    errors = errors.decode('UTF-8').split(' ')[0]
    print(list, filtered, errors)
    user_token = current_user.get_token()
    data = jsonify({'history_id': history_id,
                    'size': list,
                    'filtered': filtered,
                    'errors': errors})
    try:
        cmd = '''curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{}' -H "Authorization: Bearer {}" gimel.compbio.ucsf.edu:5020/api/_write_job_results'''.format(
            data, user_token)
        curl_cmd = shlex.split(cmd)
        os.system(curl_cmd)
        return {"message": "Curl cmd success!"}, 200
    except Exception as e:
        return {"message": "Curl cmd Failed"}, 400
if __name__=='__main__':
    main()