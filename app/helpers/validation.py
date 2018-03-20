import os
from hurry.filesize import size, alternative

from app import app
from app.data.models.format import FileFormatModel
from werkzeug.utils import secure_filename
from flask_login import current_user
from app.data.models.history import UploadHistoryModel
import pathlib


def validate(file, form):
    file_size = 0
    if file.mimetype.startswith('text/plain'):
        formats = FileFormatModel.find_all()
        line_number = 0
        lines = file.readlines()
        if len(lines) == 1:
            lines = lines[0].split(b'\r')
        for line in lines:
            line_number += 1
            if line_number > 100:
                break

            try:
                cols = line.decode('windows-1252').strip().split('\t')
                if len(cols) >= len(formats):
                    for idx, input_format in enumerate(formats):
                        obj = str
                        if input_format.col_type.lower().startswith("int"):
                            obj = int
                        elif input_format.col_type.lower().startswith("float"):
                            obj = float
                        if not isinstance(cols[idx], obj):
                            return {'message': "Type error on the line #{}".format(line_number)}, 400
                else:
                    return {'message': "Columns must be at least {}".format(len(formats))}, 400
            except:
                return {'message': "Type error on the line #{}".format(line_number)}, 400

    try:
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file_size = size(file_length, system=alternative)
        history = UploadHistoryModel(current_user.id, secure_filename(file.filename), file_size)
        history.type = form.type.data
        history.purchasability = form.purchasability.data
        history.natural_products = form.natural_products.data
        history.save_to_db()
        file_dir = os.path.realpath(os.path.dirname(app.config['UPLOAD_FOLDER'] + "/" + current_user.username+"/"))
        pathlib.Path(file_dir).mkdir(parents=True, exist_ok=True)
        file.stream.seek(0)
        file.save(os.path.join(file_dir, secure_filename(history.file_name)))
    except:
        return {"message": "An error occured inserting the file."}, 500

    return {'message': "File Uploaded! File Size:{}".format(file_size)}, 200
