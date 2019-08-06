#!/usr/bin/env python
# -*- tab-width:4;indent-tabs-mode:f;show-trailing-whitespace:t;rm-trailing-spaces:t -*-
# vi: set ts=4 et sw=4:
from __future__ import print_function
import os, sys, json
import shutil
import re
import subprocess
import logging
import argparse

UPDATE_CMD = "/mnt/nfs/home/khtang/code/upload_wizard_codes/update_zincload_status.pl"
ZINC_CATALOG_LIST = "/nfs/home/khtang/code/upload_wizard_codes/catalog_shortname.txt"

# def create_parser():
#     this_parser = argparse.ArgumentParser(description='Get shortname for loading and load catalog to ZINC')
#
#     #add arguments
#     # this_parser.add_argument('Path', metavar='-path', type=str, help='Job directory')
#
#     this_parser.add_argument('--skip-loading','-s', type=str, help='Only produce shortname, skip loading')
#
#     my_args = this_parser.parse_args(['--skip-loading'])
#     return my_args

def record_log():
    pass


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
    #is_np = job_info['natural_products'] # true or false
    short_name = ""
    #if is_np:
    #    print("This is the natural product catalog")
    #    short_name = company_basename + "np"
    if catalog_type == 'both' or catalog_type == 'sc':
        short_name = company_basename
    else:
        short_name = company_basename + catalog_type
        if availability == 'demand':
            short_name = short_name + '-v'
    return short_name

def is_qsub_running(folder):
    jobID_path = os.path.join(folder, "jobID")
    #jobID = ''
    with open(jobID_path, 'r') as fh:
       jobID = fh.read()
       fh.close()
    jobID = re.sub('[^0-9]', '', jobID)
    qstat_cmd = 'qstat | grep {0} | wc -l'.format(jobID)
    print(qstat_cmd)
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

def is_catalog_exist_on_zinc(shortname):
    with open(ZINC_CATALOG_LIST, 'r') as fh:
        catalog_list = fh.readlines()
    if shortname not in catalog_list:
        cmd = UPDATE_CMD + " " + "13"
        os.system(cmd)
        return False
    else:
        return True

def main():

    # args = create_parser()
    job_folder = os.path.abspath(sys.argv[1])
    os.chdir(job_folder)
    job_info = parse_job_info()
    catalog_shortname = get_catalog_shortname(job_info)
    print('The SHORT NAME is ' + catalog_shortname)

    if is_catalog_exist_on_zinc(catalog_shortname):
        if is_qsub_running(job_folder):
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
                    shutil.move(smile_file, "{0}/{1}".format(catalog_shortname, ism_file))
                    os.chdir(catalog_shortname)
                    source_cmd = "source /mnt/nfs/ex9/work/khtang/cmd"
                    source = subprocess.Popen(source_cmd, shell=True)
                    source.communicate()
                    submit_cmd = "sh /mnt/nfs/ex9/work/khtang/batch {0}".format(ism_file)
                    print("Submitting job to the cluster...")
                    submit_job = subprocess.Popen(submit_cmd, shell=True)
                    submit_job.communicate()
                    cmd = UPDATE_CMD + " " + "7"
                    os.system(cmd)
                except Exception as e:
                    cmd = UPDATE_CMD + " " + "6"
                    os.system(cmd)
    else:
        sys.exit(1)




if __name__=="__main__":
    main()
