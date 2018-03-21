from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, BooleanField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class UploadForm(FlaskForm):
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['txt', 'gzip', 'zip'], 'Please upload only allowed files! (.txt, .gzip, .zip)')
    ])
    type = SelectField(
        'Type',
        choices=[('bb', 'Building Block'), ('sc', 'Screening Compounds'), ('both', 'Mixed')]
    )
    purchasability = SelectField(
        'Purchasability',
        choices=[('stock', 'In Stock'), ('demand', 'Make on Demand')]
    )
    natural_products = BooleanField('Natural products')
    submit = SubmitField('submit')
