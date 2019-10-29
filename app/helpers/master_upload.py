import os, shutil
from flask import current_app
from hurry.filesize import size, alternative
from app.data.models.format import FileFormatModel
from werkzeug.utils import secure_filename
from flask_login import current_user
from app.data.models.history import UploadHistoryModel
from app.data.models.company import CompanyModel
from app.data.models.user import UserModel
from app.data.models.job_log import JobLogModel
from app.data.models.field import FieldModel
from app.data.models.field_allowed_value import FieldAllowedValueModel
from app.data.models.field_decimal import FieldDecimalModel
import pathlib
import sys
import subprocess
import numbers
from app import db, create_app
from flask import request, jsonify, Response

from datetime import datetime, timezone
import time
import json, csv
from botocore.client import Config
import boto3
import flask_excel as excel
from collections import OrderedDict
from pdb import set_trace
from app.helpers.upload_tools import get_user_job_count
# from app.main.catalog_jobs_routes import utc_to_local



ALLOWED_EXTENSIONS = set(['bz2', '7z', 'tar', 'gz', 'zip', 'sdf', 'txt', 'smi', 'csv', 'tsv'])
ALLOWED_EXTENSIONS2 = set(['tsv', 'xls', 'xlsx', 'xlsm', 'csv'])

config = Config(connect_timeout=5, retries={'max_attempts': 0})
app = create_app()
s3 = boto3.client(
    "s3",
    config=config,
    aws_access_key_id=app.config['S3_KEY'],
    aws_secret_access_key=app.config['S3_SECRET']
)

s3_res = boto3.resource(
    "s3",
    config=config,
    aws_access_key_id=app.config['S3_KEY'],
    aws_secret_access_key=app.config['S3_SECRET']
)


def get_miliseconds():
    (dt, micro) = datetime.utcnow().strftime('%Y%m%d%H%M%S.%f').split('.')
    dt = "%s%03d" % (dt, int(micro) / 1000)
    return dt


def upload_file_to_s3(file, file_name, dir_name, acl="public-read"):
    try:
        # dir_name = "company-logos"
        content_type = file.content_type
        if allowed_file2(file.filename):
            # dir_name = "raw-data"
            content_type = "application/csv; charset=utf-8"
            file_name = "{}/{}.csv".format(dir_name, file_name)
        else:
            file_name = "{}/{}_{}".format(dir_name, get_miliseconds(), file_name.replace(" ", "_"))

        s3.upload_fileobj(
            file,
            current_app.config['S3_BUCKET'],
            file_name,
            ExtraArgs={
                "ACL": acl,
                "ContentType": content_type
            }
        )
    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return None
    return "http://{}.s3.amazonaws.com/{}".format(current_app.config["S3_BUCKET"], file_name)


def upload_data_to_s3(data, filename, dir_name, acl="public-read"):
    file_name = "{}/{}.csv".format(dir_name, filename)
    try:
        s3.put_object(Body=data, Bucket=current_app.config["S3_BUCKET"], Key=file_name)

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    return "http://{}.s3.amazonaws.com/{}".format(current_app.config["S3_BUCKET"], file_name)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file2(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS2


def is_duplicate_upload(form):
    now = time.time()
    past_uploads = UploadHistoryModel.get_all_user_id(current_user.id)
    upload_file = form.file.data
    for upload in past_uploads:
        if upload_file.filename == upload.file_name:
            return upload
        else:
            return None


def validate(file, form):
    if file and allowed_file(file.filename):
        pass
        # if file.mimetype.startswith('text/plain'):
        #     formats = FileFormatModel.find_all()
        #     line_number = 0
        #     lines = file.readlines()
        #     if len(lines) == 1:
        #         lines = lines[0].split(b'\r')
        #     for line in lines:
        #         line_number += 1
        #         if line_number > 100:
        #             break
        #         try:
        #             cols = line.decode('windows-1252').strip().split('\t')
        #             if len(cols) >= len(formats):
        #                 for idx, input_format in enumerate(formats):
        #                     obj = str
        #                     if input_format.col_type.lower().startswith("int"):
        #                         obj = int
        #                     elif input_format.col_type.lower().startswith("float"):
        #                         obj = float
        #                     if not isinstance(cols[idx], obj):
        #                         return {'message': "Type error on the line #{}".format(line_number)}, 400
        #             else:
        #                 return {'message': "Columns must be at least {}".format(len(formats))}, 400
        #         except:
        #             return {'message': "Type error on the line #{}".format(line_number)}, 400
    else:
        return {"message": "Invalid file format!"}, 400

    try:
        duplicate_upload = is_duplicate_upload(form)
        if duplicate_upload is None:
            file.seek(0, os.SEEK_END)
            file_length = file.tell()
            file_size = size(file_length, system=alternative)
            history = UploadHistoryModel(current_user.id, secure_filename(file.filename), file_size)
            history.catalog_type = form.catalog_type.data
            if form.catalog_type.data == 'bio' or form.catalog_type.data == 'np':
                history.availability = 'stock'
            else:
                history.availability = form.availability.data
            history.upload_type = form.upload_type.data
            history.save_to_db()
            if current_user.has_role['Admin']:
                print("Saving additional information specified by admin ... ")
                info_dict = {}
                short_name = form.short_name.data
                if form.price_fiel.data:
                    if form.availability.data == 'demand':
                        short_name = short_name.split('-')[0]
                        econ = short_name + "e-v"
                        std = short_name + "-v"
                        prem = short_name +"p-v"
                    else:
                        econ = short_name + "e"
                        std = short_name
                        prem = short_name + "p"
                    shortname_list = [ econ, std, prem ]
                    info_dict.update({'short_name' : shortname_list})
                else:
                    info_dict.update({'short_name' : short_name})
                info_dict.update({''})


            result = save_file(file, history, history.file_name, False, history.id)
            file_info = "File Uploaded! File Size:{}. ".format(file_size)
            if result is None:
                history.delete_from_db()
                return {"message": file_info}, 200
            elif result[1] == 200:
                return {"message": file_info + result[0]["message"]}, 200
            else:
                return result
        else:
            return {"message": "File {} had been uploaded before on {}".format(duplicate_upload.file_name, duplicate_upload.date_uploaded.replace(tzinfo= timezone.utc).astimezone(tz=None).strftime("%B %d %Y at %I:%M %p"))}, 500

    except:
        print(sys.exc_info())
        return {"message": "An error occured inserting the file."}, 500

    return {"message": "File Uploaded! File Size:{}".format(file_size)}, 200




def write_json_file(history, folder):
    job_info = history.json()
    shortname = job_info['short_name']
    # job_info.update({'company_basename': current_user.short_name})
    price_tag = history.user.company.price
    if price_tag:
        if shortname.endswith('-v'):
            shortname = shortname.strip('-v')
            econ = shortname + "e-v"
            std = shortname + '-v'
            prem = shortname + 'p-v'
        else:
            econ = shortname +'e'
            std = shortname
            prem = shortname + 'p'
        shortname_list = [ econ, std, prem ]
        job_info.update({'short_name': shortname_list})
        job_info.update({'price_tag' : price_tag})
    print(job_info)
    file_path = os.path.join(folder, 'JOB_INFO.json')
    with open(file_path, 'w') as fh:
        json.dump(job_info, fh, indent=4)
        fh.close()


def check_img_type(file):
    if file.mimetype.startswith('image/jpeg') or file.mimetype.startswith('image/png'):
        return True
    else:
        return False


def process_delimited_file(delimited_file, job_folder, history):

    try:
        catalog_file = job_folder +'/'+delimited_file
        if delimited_file.endswith('csv'):
            catalog_delimiter = ','
        elif delimited_file.endswith('tsv'):
            catalog_delimiter = '\t'
        with open(catalog_file, encoding = "ISO-8859-1") as catalog:
            catalog_reader = csv.DictReader(catalog, delimiter=catalog_delimiter)
            catalog_reader = list(catalog_reader)

            catalog.close()
        smi_file = job_folder+"/"+ delimited_file.split('.')[0] + ".smi"
        product_col_name = current_user.company.idnumber
        smiles_col_name = current_user.company.smiles
        with open(smi_file, 'w') as file_handler:
            for row in catalog_reader:
                product_id = row[product_col_name]
                smiles_code = row[smiles_col_name]
                line = smiles_code + '\t' + product_id + '\n'
                file_handler.write(line)
            file_handler.close()
    except IOError:
        history.delete_from_db()
        remove_job_folder(history.id)
        # return {"message": "2: " + str(sys.exc_info()[0])}, 500

    update_status_cmd = current_app.config['SCRIPT_DIR'] + "/update_zincload_status.pl" + " 4" + " " + job_folder
    os.system(update_status_cmd)
    # return {"message": "Your job has been successfully validated!"}, 200


# def admin_save_file(file, object, name, filename, id=""):
#     try:
#         if filename.endswith('.txt'):
#             filename = filename.replace("txt", "smi")
#         admin_folder = str(current_user.id) + "_" + current_user.username
#         folder= current_app.config['UPLOAD_FOLDER'] + admin_folder
#         file_dir = os.path.realpath(os.path.dirname(folder))
#         pathlib.Path(file_dir).mkdir(parents=True, exist_ok=True)
#         file.stream.seek(0)
#         print("Saving admin upload file to directory")
#         file.save(os.path.join(file_dir, secure_filename(name)))
#         try:
#             if name.endswit
#
#     except:
#         pass
#     pass

def save_file(file, object, name, is_logo, id=""):
    try:
        if is_logo:
            folder = current_app.config['LOGO_UPLOAD_FOLDER']
            name = name.replace(" ", "_") + os.path.splitext(file.filename)[1]
        else:
            #if name.endswith(".csv"):
            #    print("csv format catalog")
            #    extract_molcules_info_from_csv(name)
            if name.endswith(".txt"):
                print("Txt format catalog")
                name = name.replace("txt", "smi")
            if name.endswith(".smi"):
                print("Smi format catalog")
            user_folder = str(current_user.id) + "_"
            if current_user.short_name and current_user.has_role("Vendor"):
                user_folder += current_user.short_name
            else:
                user_folder += "vendor"
            if  current_user.has_role("Admin"):
                user_folder += current_user.username

            user_folder += "/" + str(id) + "/"
            folder = current_app.config['UPLOAD_FOLDER'] + user_folder
        file_dir = os.path.realpath(os.path.dirname(folder))
        pathlib.Path(file_dir).mkdir(parents=True, exist_ok=True)
        file.stream.seek(0)
        # print(name)
        # print(secure_filename(name))
        # print(os.path.join(file_dir, secure_filename(name)))
        print("Saving file to directory")
        file.save(os.path.join(file_dir, secure_filename(name)))
        try:
            if name.endswith(".csv") or name.endswith(".tsv"):
                    print("delimited format catalog")
                    process_delimited_file(name, file_dir, object)
                    print("Saving json file")
                    write_json_file(object, file_dir)
                    return {"message": "Your job has been submitted!"}, 200
            print("Saving json file")
            write_json_file(object, file_dir)
        except:
            object.delete_from_db()
            remove_job_folder(object.status_id)
            return {"message": "4: " + str(sys.exc_info()[0])}, 500

    except:
        object.delete_from_db()
        remove_job_folder(object.status_id)
        return {"message": "3: " + str(sys.exc_info()[0])}, 500

    if is_logo:
        return name
    else:
        str_mandatory_columns = FileFormatModel.find_all_mandatory_column_str()
        print("Mandatory : " + str_mandatory_columns)
        str_optional_columns = FileFormatModel.find_all_optional_column_str()
        print("Optional : " + str_optional_columns)

        return run_bash_script(user_folder, str_mandatory_columns, str_optional_columns, id, object)

    return None


def remove_job_folder(id=""):
    try:
        user_folder = str(current_user.id) + "_"
        if current_user.short_name:
            user_folder += current_user.short_name
        else:
            user_folder += "vendor"
        user_folder += "/" + str(id) + "/"
        folder = current_app.config['UPLOAD_FOLDER'] + user_folder
        job_dir = os.path.realpath(os.path.dirname(folder))
        shutil.rmtree(job_dir)
    except:
        print(sys.exc_info())

def run_bash_script(user_folder, str_mandatory_columns, str_optional_columns, history_id, history):
    try:
        # print(current_user.get_token())
        # print(current_user.company.idnumber)
        # print(str_mandatory_columns)
        # print(str_optional_columns)
        if len(current_user.company.idnumber) > 0:
            script_dir = current_app.config['SCRIPT_DIR']
            print(script_dir)
            os.chdir(current_app.config['UPLOAD_FOLDER']+user_folder)
            out = subprocess.Popen(["qsub " + script_dir
                                    + 'script.sh {} {} {} {} {} {}'
                                   .format(user_folder,
                                           current_user.company.idnumber.replace(" ", ","),
                                           str_mandatory_columns,
                                           str_optional_columns,
                                           current_user.get_token(),
                                           history_id) + " > jobID"], shell=True, close_fds=True)
            # print(out.communicate())
            return {"message": "Your job has been submitted!"}, 200
        history.delete_from_db()
        remove_job_folder(history_id)
        return {"message": " Please enter your IDNUMBER in the company profile section. "
                           "We need your company IDNUMBER to validate .sdf file. "}, 400

    except AttributeError:
        history.delete_from_db()
        remove_job_folder(history_id)
        return {"message": " Please enter your IDNUMBER in the company profile section. "
                           "We need your company IDNUMBER to validate .sdf file. "}, 400

    except:
        history.delete_from_db()
        remove_job_folder(history_id)
        print(sys.exc_info())
        return {"message": "1: " + str(sys.exc_info()[0])}, 500
