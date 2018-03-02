from app import db
from app.data.models.format import FileFormat

# def get_mandatory_field_count():


def validate(file):
    formats = FileFormat.query.order_by(FileFormat.order).all()
    line_number = 0
    for line in file.stream:
        line_number += 1
        cols = line.decode().strip().split('\t')
        if len(cols) >= len(formats):
            for idx, input_format in enumerate(formats):
                obj = str
                if input_format.col_type.lower().startswith("inte"):
                    obj = int
                elif input_format.col_type.lower().startswith("float"):
                    obj = float
                if not isinstance(cols[idx], obj):
                    return "Type error on the line #{}".format(line_number)
        else:
            return "Columns must be at least {}".format(len(formats))
    return "File Uploaded. Total line(s): {}".format(line_number)
