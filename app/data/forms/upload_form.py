from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class UploadForm(FlaskForm):
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['txt', 'gzip', 'zip'], 'Please upload only allowed files! (.txt, .)')
    ])
    # separator =
    submit = SubmitField('Upload File')
