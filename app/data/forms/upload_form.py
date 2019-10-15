from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, BooleanField, FileField, StringField
from flask_wtf.file import FileField, FileRequired, FileAllowed, DataRequired


class UploadForm(FlaskForm):
    file = FileField('File:', render_kw={"class": "form-control btn btn-outline-info"}, validators=[
        FileRequired(),
        FileAllowed(['bz2', '7z', 'tar', 'gz', 'zip', 'sdf', 'txt', 'smi', 'csv', 'tsv', 'xlsx'],
                    'Please upload only allowed files! (.txt, .)')
    ])
    catalog_type = SelectField('Catalog Type:', render_kw={"class": "form-control m-input"}, validators=[DataRequired()],
                       choices=[('', '--- Select one ---'), ('bb', 'Building Blocks'), ('sc', 'Screening Compounds'), ('both', 'Mixed'),
                                ('np', 'Natural Products'), ('bio', 'Bioactives'), ]
    )
    availability = SelectField('Availability:',
                                 render_kw={"class": "form-control m-input"}, validators=[DataRequired()],
                                 choices=[('', '--- Select one ---'), ('stock', 'In Stock'), ('demand', 'Make on Demand')]
    )
    upload_type = SelectField('Upload Type:', render_kw={"class": "form-control m-input"}, validators=[DataRequired()],
                              choices=[('', '--- Select one ---'), ('full', 'Full Catalog Update'), ('incremental', 'Incremental Catalog Update')]
                              )
    # natural_products = BooleanField(' Natural products')
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})



class MasterUploadForm(FlaskForm):
    file = FileField('File:', render_kw={"class": "form-control btn btn-outline-info"}, validators=[
        FileRequired(),
        FileAllowed(['bz2', '7z', 'tar', 'gz', 'zip', 'sdf', 'txt', 'smi', 'csv', 'tsv', 'xlsx'],
                    'Please upload only allowed files! (.txt, .)')
    ])
    catalog_type = SelectField('Catalog Type:', render_kw={"class": "form-control m-input"}, validators=[DataRequired()],
                       choices=[('', '--- Select one ---'), ('bb', 'Building Blocks'), ('sc', 'Screening Compounds'), ('both', 'Mixed'),
                                ('np', 'Natural Products'), ('bio', 'Bioactives'), ]
    )
    availability = SelectField('Availability:',
                                 render_kw={"class": "form-control m-input"}, validators=[DataRequired()],
                                 choices=[('', '--- Select one ---'), ('stock', 'In Stock'), ('demand', 'Make on Demand')]
    )
    upload_type = SelectField('Upload Type:', render_kw={"class": "form-control m-input"}, validators=[DataRequired()],
                              choices=[('', '--- Select one ---'), ('full', 'Full Catalog Update'), ('incremental', 'Incremental Catalog Update')]
                              )
    # natural_products = BooleanField(' Natural products')
    short_name = StringField('Catalog Shortname', render_kw={"class": "form-control m-input"}, validators=[DataRequired()])
    price_field = StringField('Price Field', render_kw={"class": "form-control m-input"})
    id_field = StringField('ID Field', render_kw={"class": "form-control m-input"}, validators=[DataRequired()])
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})

