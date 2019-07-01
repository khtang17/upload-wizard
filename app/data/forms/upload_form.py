from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, BooleanField, FileField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class UploadForm(FlaskForm):
    file = FileField('File:', render_kw={"class": "form-control btn btn-outline-info"}, validators=[
        FileRequired(),
        FileAllowed(['bz2', '7z', 'tar', 'gz', 'zip', 'sdf', 'txt', 'smi', 'csv', 'tsv', 'xlsx'],
                    'Please upload only allowed files! (.txt, .)')
    ])
    catalog_type = SelectField('Catalog Type:', render_kw={"class": "form-control m-input"},
                       choices=[('bb', 'Building Block'), ('sc', 'Screening Compounds'), ('both', 'Mixed')]
    )
    availability = SelectField('Availability:',
                                 render_kw={"class": "form-control m-input"},
                                 choices=[('stock', 'In Stock'), ('demand', 'Make on Demand')]
    )
    upload_type = SelectField('Upload Type:', render_kw={"class": "form-control m-input"},
                              choices=[('full', 'Full Catalog Update'), ('incremental', 'Incremental Catalog Update')]
                              )
    natural_products = BooleanField(' Natural products')
    submit = SubmitField('submit', render_kw={"class": "btn btn-success"})
