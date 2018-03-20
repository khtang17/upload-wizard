from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, BooleanField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class UploadForm(FlaskForm):
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['txt', 'gzip', 'zip'], 'Please upload only allowed files! (.txt, .)')
    ])
    type = SelectField(
        'Type',
        choices=[('bb', 'Building Block'), ('sc', 'SC'), ('mx', 'Mixed')]
    )
    purchasability = SelectField(
        'Purchasability',
        choices=[('ic', 'In Stock'), ('od', 'Make on Demand')]
    )
    natural_products = BooleanField('Natural products')
    submit = SubmitField('submit')
