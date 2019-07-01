#!/usr/bin/env python
# -*- tab-width:4;indent-tabs-mode:f;show-trailing-whitespace:t;rm-trailing-spaces:t -*-
# vi: set ts=4 et sw=4:

from __future__ import print_function
import sys, os, json
import subprocess

def get_job_info_from_json(file):
    file_path = os.path.abspath(file)
    with open(file_path, 'r') as fh:
        job_info = json.load(fh)
    short_name = job_info.get("short_name")
    catalog_type = job_info.get("catalog_type")
    upload_type = job_info.get("upload_type")
    return short_name, catalog_type, upload_type


def main():
    json_file = sys.argv[1]
    short_name, catalog_type, upload_type = get_job_info_from_json(json_file)

    if short_name is not None:
        sys.exit(1)
    else:
        print("Short name is " + str(short_name))
        print("")
        print("Run depletion...")
        # out = subprocess.Popen("zinc-manage -e admin admin catalogs deplete -C 10000 {} list2".format(short_name), shell=True, close_fds=True)
    print(short_name, catalog_type, upload_type)
if __name__=="__main__":
    main()