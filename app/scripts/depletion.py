#!/usr/bin/env python
# -*- tab-width:4;indent-tabs-mode:f;show-trailing-whitespace:t;rm-trailing-spaces:t -*-
# vi: set ts=4 et sw=4:

from __future__ import print_function
import sys, os, json
import argparse
import subprocess
import shutil


cmd = "python depletion.py <job_dir>"
UPDATE_CMD = "/mnt/nfs/home/khtang/code/upload_wizard_codes/update_zincload_status.pl"

def get_catalog_shortname(job_info):
    company_basename = job_info['company_basename']
    catalog_type = job_info['catalog_type'] # SC, BB, or both
    availability = job_info['availability'] # stock or demand
    upload_type = job_info['upload_type']
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
        if upload_type == 'incremental':
                short_name = None
    return short_name

def get_job_info_from_json(folder):
    file_path = os.path.join(folder, "JOB_INFO.json")
    with open(file_path, 'r') as fh:
        job_info = json.load(fh)
    short_name = get_catalog_shortname(job_info)
    catalog_type = job_info.get("catalog_type")
    upload_type = job_info.get("upload_type")
    return short_name, catalog_type, upload_type


def main():
    job_dir = sys.argv[1]
    short_name, catalog_type, upload_type = get_job_info_from_json(job_dir)

    if short_name is None:
        print("This is a incremental upload")
        sys.exit(1)
    else:
        print("This is a full upload")
        print("Short name is " + str(short_name))
        os.chdir(short_name)
        print("Run depletion...")
        cmd = "zinc-manage -e admin admin catalogs deplete -C 10000 {} list2".format(str(short_name))
        print(cmd)
        out = subprocess.Popen("zinc-manage -e admin admin catalogs deplete -C 10000 {} list2".format(short_name), shell=True, close_fds=True)
        out.communicate()[0]
        cmd = UPDATE_CMD + " " + "10"
        os.system(cmd)
if __name__=="__main__":
    main()
