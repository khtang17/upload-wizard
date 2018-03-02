import os

from app import app
from app.data.models.format import FileFormatModel
from werkzeug.utils import secure_filename
from flask_login import current_user
from app.data.models.history import UploadHistoryModel


def validate(file):
    formats = FileFormatModel.find_all()
    line_number = 0
    for line in file.stream:
        line_number += 1
        cols = line.decode().strip().split('\t')
        if len(cols) >= len(formats):
            for idx, input_format in enumerate(formats):
                obj = str
                if input_format.col_type.lower().startswith("int"):
                    obj = int
                elif input_format.col_type.lower().startswith("float"):
                    obj = float
                if not isinstance(cols[idx], obj):
                    return "Type error on the line #{}".format(line_number)
        else:
            return "Columns must be at least {}".format(len(formats))

    history = UploadHistoryModel(current_user.id, secure_filename(file.filename))
    history.save_to_db()
    print(app.instance_path)
    file.save(os.path.join(
        app.instance_path, 'files', history.file_name
    ))
    return "File Uploaded. Total line(s): {}".format(line_number)
