#!/usr/bin/env python
# -*- tab-width:4;indent-tabs-mode:f;show-trailing-whitespace:t;rm-trailing-spaces:t -*-
# vi: set ts=4 et sw=4:
from __future__ import print_function
import os, sys, json
import shutil
import re
import subprocess

UPDATE_CMD = "/mnt/nfs/home/khtang/code/upload_wizard_codes/update_zincload_status.pl"

def parse_job_info():
    json_path = "JOB_INFO.json"
    try:
        with open(json_path, "r") as json_file:
            job_info = json.load(json_file)
        return job_info
    except IOException as e:
        print(e)
def get_catalog_shortname(job_info):
    company_basename = job_info['company_basename']
    catalog_type = job_info['catalog_type'] # SC, BB, or both
    availability = job_info['availability'] # stock or demand
    is_np = job_info['natural_products'] # true or false
    short_name = ""
    if is_np:
        print("This is the natural product catalog")
        short_name = company_basename + "np"
    else:
        if catalog_type == 'both':
            short_name = company_basename
        else:
            short_name = company_basename + catalog_type
            if availability == 'demand':
                short_name = short_name + '-v'
    return short_name

def is_qsub_running():
    jobID_path = os.path.join(os.getcwd(), "jobID")
    jobID = ''

    try:
        with open(jobID_path, 'r') as fh:
            jobID = fh.read()
            fh.close()
        jobID = re.sub('[^0-9]', '', jobID)
    except IOException as e:
        print(e)
    qstat_cmd = "qstat | grep {} | wc -l".format(jobID)
    check = subprocess.Popen(qstat_cmd, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)
    running = check.communicate()[0].decode('utf-8')
    remain = re.sub('[^0-9]','', running)
    print(remain)
    if int(remain) == 0:
        return False
    else:
        return True

def check_file(job_folder, file_type):
    file_list = os.listdir(job_folder)
    smi_file = ''
    for file in file_list:
        if file.endswith(file_type):
            print("smiles file found!")
            smi_file = file

    return smi_file


def main():
    job_folder = os.path.abspath(sys.argv[1])
    os.chdir(job_folder)
    print(os.getcwd())
    job_info = parse_job_info()
    catalog_shortname = get_catalog_shortname(job_info)
    print(catalog_shortname)
    if is_qsub_running():
        print("qsub is still running")
    else:
        print("qsub is done")
        smile_file = check_file(job_folder, "smi")
        if not smile_file:
            cmd = UPDATE_CMD + " " + '3'  # marked validation failed
            os.system(cmd)
        else:
            print(smile_file)
            cmd = UPDATE_CMD + " " + "5"
            os.system(cmd)
            try:
                os.makedirs(catalog_shortname)
                ism_file = catalog_shortname+".ism"
                shutil.move(smile_file, "{}/{}".format(catalog_shortname, ism_file))
                os.chdir(catalog_shortname)
                print(os.getcwd())
                os.system("source /mnt/nfs/ex9/work/khtang/cmd")
                submit_cmd = "sh /mnt/nfs/ex9/work/khtang/batch {}".format(ism_file)
                print(submit_cmd)
                submit_job = subprocess.Popen(submit_cmd, shell=True)
                submit_job.communicate()
                cmd = UPDATE_CMD + " " + "7"
                os.system(cmd)
            except Exception as e:
                cmd = UPDATE_CMD + " " + "6"
                os.system(cmd)



if __name__=="__main__":
    main()