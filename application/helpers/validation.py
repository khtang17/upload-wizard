import os
from flask import current_app
from hurry.filesize import size, alternative
from application.data.models.format import FileFormatModel
from werkzeug.utils import secure_filename
from flask_login import current_user
from application.data.models.history import UploadHistoryModel
from application.data.models.catalog import CatalogModel
from application.data.models.job_log import JobLogModel
from application.data.models.field import FieldModel
from application.data.models.field_allowed_value import FieldAllowedValueModel
from application.data.models.field_decimal import FieldDecimalModel
import pathlib
import sys
import subprocess
import numbers
from application import db
from flask import request, jsonify


ALLOWED_EXTENSIONS = set(['bz2', '7z', 'tar', 'gz', 'zip', 'sdf', 'txt', 'smi'])
ALLOWED_EXTENSIONS2 = set(['tsv', 'xls', 'xlsx', 'xlsm', 'csv'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file2(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS2


def validate(file, form):
    if file and allowed_file(file.filename):
        test=""
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
        history.type = form.type.data
        history.purchasability = form.purchasability.data
        history.natural_products = form.natural_products.data
        history.save_to_db()
        result = save_file(file, history.file_name, False, history.id)
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


def check_img_type(file):
    if file.mimetype.startswith('image/jpeg') or file.mimetype.startswith('image/png'):
        return True
    else:
        return False


def save_file(file, name, is_logo, id=""):
    try:
        if is_logo:
            folder = current_app.config['LOGO_UPLOAD_FOLDER']
            name = name.replace(" ", "_") + os.path.splitext(file.filename)[1]
        else:
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
        print(name)
        print(secure_filename(name))
        file.save(os.path.join(file_dir, secure_filename(name)))
    except:
        print(sys.exc_info())
        return {"message": "1: " + str(sys.exc_info()[0])}, 500

    if is_logo:
        return name
    else:
        str_mandatory_columns = FileFormatModel.find_all_mandatory_column_str()
        str_optional_columns = FileFormatModel.find_all_optional_column_str()
        return run_bash_script(user_folder, str_mandatory_columns, str_optional_columns, id)

    return None


def run_bash_script(user_folder, str_mandatory_columns, str_optional_columns, history_id):
    try:
        print(current_user.get_token())
        print(current_user.company.idnumber)
        if len(current_user.company.idnumber) > 0:
            script_dir = current_app.config['UPLOAD_FOLDER'] + "script/"
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


def excel_validation(request, form):
    warning_msg = []
    error_msg = []
    mandatory_fields = [mand.field_name.lower() for mand in FieldModel.find_by_mandatory(True)]
    mandatory_field_ids = []
    optional_fields = [mand.field_name.lower() for mand in FieldModel.find_by_mandatory(False)]
    validation_row_limit = int(current_app.config['FILE_VALIDATION_LIMIT'])

    dict_value = request.get_array(field_name='file')
    if len(dict_value) <= 1:
        return {"message": "No data error!"}, 400
    headers = [h.lower() for h in dict_value[0]]
    print("headers")
    print(headers)
    diplicated_fields = set([x for x in headers if headers.count(x) > 1])
    if len(diplicated_fields) > 0:
        error_msg.append([0, "Field duplication error: {} \n".format(list(diplicated_fields))])

    if set(mandatory_fields).issubset(set(headers)):
        for m_field in mandatory_fields:
            mandatory_field_ids.append(headers.index(m_field))
        for index, item in enumerate(dict_value[1:]):
            # if validation_row_limit == index + 1:
            #     break
            for m_field_id in mandatory_field_ids:
                if not item[m_field_id]:
                    error_msg.append(["Line {}: ".format(index + 1), "Mandatory field [{}] has no value".format(headers[m_field_id])])
    else:
        error_msg.append(["", "Mandatory field missing {}".format(set(mandatory_fields)-set(headers))])

    form.file.data.seek(0, os.SEEK_END)
    file_length = form.file.data.tell()
    file_size = size(file_length, system=alternative)
    history = UploadHistoryModel(current_user.id, secure_filename(form.file.data.filename), file_size)
    history.type = form.type.data
    history.purchasability = form.purchasability.data
    history.natural_products = form.natural_products.data
    history.save_to_db()

    decimal_fields = FieldDecimalModel.find_all()
    for dec_field in decimal_fields:
        # it skips when mandatory field is missing
        try:
            field_index = headers.index(dec_field.field.field_name.lower())
        except:
            break

        if field_index:
            for row, item_list in enumerate(dict_value[1:]):
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
            for row, item_list in enumerate(dict_value[1:]):
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

    # error_msg_set.update(set([x[1] + " (same errors at the {} more lines)".format(
    #     error_msg.count(x)) for x in error_msg if error_msg.count(x) > 1]))
    # warning_msg_set.update(set([x[1] + " (same errors at the {} more lines)".format(
    #     warning_msg.count(x)) for x in warning_msg if warning_msg.count(x) > 1]))



    print("ERROR")
    print(error_msg)
    print(error_msg_set)
    print("WARNING")
    # print(warning_msg)
    print(warning_msg_set)
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

    print("line 280")
    catalog_objs = []
    for item_list in dict_value[1:]:
        for index, value in enumerate(item_list):
            if headers[index] in mandatory_fields:
                catalog_objs.append(CatalogModel(headers[index], 'mandatory', value, history.id))
            if headers[index] in optional_fields:
                catalog_objs.append(CatalogModel(headers[index], 'optional', value, history.id))

    CatalogModel.save_objects(catalog_objs)

    job_log = JobLogModel()
    job_log.status = "Finished"
    job_log.status_type = 4
    job_log.history_id = history.id
    job_log.save_to_db()
    # catalogs = CatalogModel.find_by_history_id(history.id)
    # res = {c.field_name: c.value for c in catalogs}
    # print("catalog as dict")
    # print(res)

    return {"message": "Your excel file has been submitted!"}, 200


