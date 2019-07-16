import os
from flask import current_app
from hurry.filesize import size, alternative
from app.data.models.format import FileFormatModel
from werkzeug.utils import secure_filename
from flask_login import current_user
from app.data.models.history import UploadHistoryModel
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

from datetime import datetime
import time
import json
from botocore.client import Config
import boto3
import flask_excel as excel
from collections import OrderedDict



ALLOWED_EXTENSIONS = set(['bz2', '7z', 'tar', 'gz', 'zip', 'sdf', 'txt', 'smi'])
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
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file_size = size(file_length, system=alternative)
        history = UploadHistoryModel(current_user.id, secure_filename(file.filename), file_size)
        history.catalog_type = form.catalog_type.data
        history.upload_type = form.upload_type.data
        history.availability = form.availability.data
        history.natural_products = form.natural_products.data
        history.save_to_db()
        result = save_file(file, history, history.file_name, False, history.id)
        file_info = "File Uploaded! File Size:{}. ".format(file_size)
        if result is None:
            return {"message": file_info}, 200
        elif result[1] == 200:
            return {"message": file_info + result[0]["message"]}, 200
        else:
            return result
    except:
        print(sys.exc_info())
        return {"message": "An error occured inserting the file."}, 500

    return {"message": "File Uploaded! File Size:{}".format(file_size)}, 200



def write_json_file(history, folder):
    job_info = history.json()
    job_info.update({'company_basename': current_user.short_name})
    file_path = os.path.join(folder, 'JOB_INFO.json')
    with open(file_path, 'w') as fh:
        json.dump(job_info, fh, indent=4)
        fh.close()

def check_img_type(file):
    if file.mimetype.startswith('image/jpeg') or file.mimetype.startswith('image/png'):
        return True
    else:
        return False


def save_file(file, object, name, is_logo, id=""):
    try:
        if is_logo:
            folder = current_app.config['LOGO_UPLOAD_FOLDER']
            name = name.replace(" ", "_") + os.path.splitext(file.filename)[1]
        else:
            if name.endswith(".txt"):
                print("Txt format catalog")
                name = name.replace("txt", "smi")
            if name.endswith(".smi"):
                print("Smi format catalog")
            user_folder = str(current_user.id) + "_"
            if current_user.short_name:
                user_folder += current_user.short_name
            else:
                user_folder += "vendor"
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
        print("Saving json file")
        write_json_file(object, file_dir)
    except:
        print(sys.exc_info())
        return {"message": "1: " + str(sys.exc_info()[0])}, 500

    if is_logo:
        return name
    else:
        str_mandatory_columns = FileFormatModel.find_all_mandatory_column_str()
        print("Mandatory : " + str_mandatory_columns)
        str_optional_columns = FileFormatModel.find_all_optional_column_str()
        print("Optional : " + str_optional_columns)
        return run_bash_script(user_folder, str_mandatory_columns, str_optional_columns, id)

    return None


def run_bash_script(user_folder, str_mandatory_columns, str_optional_columns, history_id):
    try:
        # print(current_user.get_token())
        # print(current_user.company.idnumber)
        # print(str_mandatory_columns)
        # print(str_optional_columns)
        if len(current_user.company.idnumber) > 0:
            script_dir = current_app.config['SCRIPT_DIR']
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
        return {"message": " Please enter your IDNUMBER in the company profile section. "
                           "We need your company IDNUMBER to validate .sdf file. "}, 400
    except AttributeError:
        return {"message": " Please enter your IDNUMBER in the company profile section. "
                           "We need your company IDNUMBER to validate .sdf file. "}, 400
    except:
        print(sys.exc_info())
        return {"message": "1: " + str(sys.exc_info()[0])}, 500


# def save_excel_file(request):
#     file = request.files['file']
#     file.seek(0, os.SEEK_END)
#     file_length = file.tell()
#     file_size = size(file_length, system=alternative)
#     history = UploadHistoryModel(current_user.id, secure_filename(file.filename), file_size)
#     history.save_to_db()
#
#     file.stream.seek(0)
#     s3_result = upload_file_to_s3(file, history.id)
#     if s3_result:
#         history.status = 2
#         history.save_to_db()

def excel_validation(request):
    start_time_whole = time.time()
    warning_msg = []
    error_msg = []

    start_time_readsql = time.time()
    mandatory_fields = [mand.field_name.lower() for mand in FieldModel.find_by_mandatory(True)]
    mandatory_field_ids = []
    optional_fields = [mand.field_name.lower() for mand in FieldModel.find_by_mandatory(False)]
    validation_row_limit = int(current_app.config['FILE_VALIDATION_LIMIT'])
    end_readsql = time.time()
    elapsed_readsql = end_readsql - start_time_readsql
    print("read SQL spent {} seconds".format(elapsed_readsql))

    start_time_readasarray = time.time()
    dict_value = request.get_array(field_name='file')
    end_readasarray = time.time()
    elapsed_readasarray = end_readasarray - start_time_readasarray
    print("Read as ARRAY  spent {} seconds".format(elapsed_readasarray))
    if len(dict_value) <= 1:
        return {"message": "No data error!"}, 400
    headers = [h.lower() for h in dict_value[0]]
    print("headers")
    print(headers)
    duplicated_fields = set([x for x in headers if headers.count(x) > 1])
    if len(duplicated_fields) > 0:
        error_msg.append([0, "Field duplication error: {} \n".format(list(duplicated_fields))])

    if set(mandatory_fields).issubset(set(headers)):
        for m_field in mandatory_fields:
            mandatory_field_ids.append(headers.index(m_field))
        for index, item in enumerate(dict_value[1:validation_row_limit]):
            for m_field_id in mandatory_field_ids:
                if not item[m_field_id]:
                    error_msg.append(["Line {}: ".format(index + 1), "Mandatory field [{}] has no value".format(headers[m_field_id])])
    else:
        error_msg.append(["", "Mandatory field missing {}".format(set(mandatory_fields)-set(headers))])

    file = request.files['file']
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file_size = size(file_length, system=alternative)
    history = UploadHistoryModel(current_user.id, secure_filename(file.filename), file_size)
    # No need to add miliseconds for this file name because it was saved to s3 with history id
    history.file_name = secure_filename(file.filename)
    # history.data_array = str(request.get_array(field_name='file'))
    history.save_to_db()

    decimal_fields = FieldDecimalModel.find_all()
    for dec_field in decimal_fields:
        # it skips when mandatory field is missing
        try:
            field_index = headers.index(dec_field.field.field_name.lower())
        except:
            break

        if field_index:
            for row, item_list in enumerate(dict_value[1:validation_row_limit]):
                if isinstance(item_list[field_index], numbers.Real):
                    if float(item_list[field_index]) < dec_field.min_val:
                        error_msg.append(["Line {}: ".format(row + 1),
                                          "[{}] field value must be "
                                          "greater than {}".format(headers[field_index], dec_field.min_val)])
                        # error_msg += "Line{}: [{}] field value must be greater " \
                        #              "than {} \n".format(row + 1, headers[ field_index], dec_field.min_val)
                    if float(item_list[field_index]) > dec_field.max_val:
                        warning_msg.append(["Line {}: ".format(row + 1),
                                            "[{}] field value is greater "
                                            "than max value: {}".format(headers[field_index], dec_field.max_val)])
                        # warning_msg += "Line{}: [{}] field value was greater " \
                        #              "than max value: {}.\n".format(row + 1, headers[field_index], dec_field.max_val)
                    dict_value[row+1][field_index] = "{0:.2f}".format(item_list[field_index])
                else:
                    error_msg.append(["Line {}: ".format(row + 1),
                                      "[{}] field has invalid data".format(headers[field_index])])
                    # error_msg += "Line{}: [{}] field has invalid data \n".format(row + 1, headers[field_index])

    string_fields = FieldAllowedValueModel.find_all()
    for str_field in string_fields:
        # it skips when mandatory field is missing
        try:
            field_index = headers.index(str_field.field.field_name.lower())
        except:
            break

        if field_index:
            for row, item_list in enumerate(dict_value[1:validation_row_limit]):
                try:
                    if str(item_list[field_index]).lower() not in \
                            [str(x.strip().lower()) for x in str_field.allowed_values.split(',')]:
                        error_msg.append(["Line {}: ".format(row + 1),
                                          "[{}] field value is not allowed".format(headers[field_index])])
                        # error_msg += "Line{}: [{}] field value is not allowed".format(row + 1, headers[field_index])
                except:
                    error_msg.append(["Line {}: ".format(row + 1),
                                      "[{}] field allowed values has an error. "
                                      "Please contact admin to fix this issue.".format(headers[field_index])])
                    # error_msg += "Line{}: [{}] field allowed values has an error. " \
                    #              "Please contact admin to fix this issue.".format(row + 1, headers[field_index])

    # error_msg_set = set(["{} {}".format(x[0], x[1]) for x in error_msg if error_msg.count(x) == 1])
    # warning_msg_set = set(["{} {}".format(x[0], x[1]) for x in warning_msg if warning_msg.count(x) == 1])

    error_msg_set = set(["{} {}".format(min([y[0] for y in error_msg if y[1] == x[1]]), x[1])
                         for x in error_msg if len([y for y in error_msg if y[1] == x[1]]) == 1])
    warning_msg_set = set(["{} {}".format(min([y[0] for y in warning_msg if y[1] == x[1]]), x[1])
                           for x in warning_msg if len([y for y in warning_msg if y[1] == x[1]]) == 1])

    error_msg_set.update(set(["{} {}  (same errors occurred {} other lines)".format(
        [y[0] for y in error_msg if y[1] == x[1]][0], x[1], len([y for y in error_msg if y[1] == x[1]]))
                     for x in error_msg if len([y for y in error_msg if y[1] == x[1]]) > 1]))
    warning_msg_set.update(set(["{} {}  (same errors occurred {} other lines)".format(
        [y[0] for y in warning_msg if y[1] == x[1]][0], x[1], len([y for y in warning_msg if y[1] == x[1]]))
        for x in warning_msg if len([y for y in warning_msg if y[1] == x[1]]) > 1]))

    # catalog_objs = []
    # catalog_dict = []
    str_data = ""
    # print(mandatory_fields)
    for item_list in dict_value:
        data_dict = {}
        for index, value in enumerate(item_list):
            if headers[index] in mandatory_fields:
                data_dict[mandatory_fields.index(headers[index])] = value
                # catalog_objs.append(CatalogModel(headers[index], 'mandatory', value, history.id))
                # catalog_dict.append(
                #     dict(field_name=headers[index], type='mandatory', value=value, history_id=history.id))
            if headers[index] in optional_fields:
                # used mandatory_fields.count()+index) in order to place optional field after mandatory fields
                # print(len(mandatory_fields)+index)
                data_dict[len(mandatory_fields)+index] = value
            # catalog_objs.append(CatalogModel(headers[index], 'optional', value, history.id))
            # catalog_dict.append(
            #     dict(field_name=headers[index], type='optional', value=value, history_id=history.id))

        str_line = ','.join(str(data_dict[key]) for key in sorted(data_dict.keys()))
        str_data = str_data + str_line + '\n'

    s3_dir = "validated"
    history.status = 1
    if error_msg:
        s3_dir = "validation-error"
        history.status = 2

    # Unvalidated
    # s3_dir = "unvalidated"
    # history.status = 3
    history.save_to_db()

    start_time_s3 = time.time()
    file.stream.seek(0)
    # s3_result = upload_file_to_s3(file, history.id, s3_dir)
    upload_data_to_s3(str_data, history.id, s3_dir)
    end_s3 = time.time()
    elapsed_s3 = end_s3 - start_time_s3
    print("S3 upload spent {} seconds".format(elapsed_s3))





    if warning_msg:
        job_log = JobLogModel()
        job_log.status = '<br>'.join(str(s) for s in warning_msg_set)
        job_log.status_type = 2
        job_log.history_id = history.id
        job_log.save_to_db()

    if error_msg:
        job_log = JobLogModel()
        job_log.status = '<br>'.join(str(s) for s in error_msg_set)
        job_log.status_type = 3
        job_log.history_id = history.id
        job_log.save_to_db()
        job_log = JobLogModel()
        job_log.status = "Finished"
        job_log.status_type = 4
        job_log.history_id = history.id
        job_log.save_to_db()
        return {"message": '<br>'.join(str(s) for s in error_msg_set)}, 400

    job_log = JobLogModel()
    job_log.status = "Finished"
    job_log.status_type = 4
    job_log.history_id = history.id
    job_log.save_to_db()

    end_whole = time.time()
    elapsed_whole = end_whole - start_time_whole
    print("Whole process spent {} seconds without file uploading".format(elapsed_whole))
    return {"message": "Your excel file has been submitted!"}, 200

