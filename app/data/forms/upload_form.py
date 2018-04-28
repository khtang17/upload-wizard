from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, BooleanField, FileField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class UploadForm(FlaskForm):
    file = FileField('File:', render_kw={"class": "form-control btn btn-outline-info"}, validators=[
        FileRequired(),
        FileAllowed(['bz2', '7z', 'tar', 'gz', 'zip', 'sdf', 'txt', 'smi', 'csv', 'tsv'],
                    'Please upload only allowed files! (.txt, .)')
    ])
    type = SelectField('Type:', render_kw={"class": "form-control m-input"},
                       choices=[('bb', 'Building Block'), ('sc', 'Screening Compounds'), ('both', 'Mixed')]
    )
    purchasability = SelectField('Purchasability:',
                                 render_kw={"class": "form-control m-input"},
                                 choices=[('stock', 'In Stock'), ('demand', 'Make on Demand')]
    )
    natural_products = BooleanField(' Natural products')
    submit = SubmitField('submit', render_kw={"class": "btn btn-success"})
