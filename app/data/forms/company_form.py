from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email
from flask_wtf.file import FileField, FileAllowed


class CompanyForm(FlaskForm):
    id = HiddenField('Company ID')
    file = FileField('Company Logo', validators=[
        FileAllowed(['png', 'jpeg', 'jpg'], 'Please upload only allowed files! (.txt, .jpeg, .jpg)')
    ])
    logo = HiddenField('Logo')
    name = StringField('Company Name*', validators=[DataRequired()])
    description = TextAreaField('Company Description*', render_kw={"rows": 9}, validators=[DataRequired()])
    address = TextAreaField('Company Address*', render_kw={"rows": 5}, validators=[DataRequired()])
    telephone_number = StringField('Telephone Number*', validators=[DataRequired()])
    toll_free_number = StringField('Toll Free Number')
    fax_number = StringField('Fax Number')
    website = StringField('Website')
    sales_email = StringField('Sales Email')
    personal_contact_name = StringField('Personal Contact name')
    personal_contact_email = StringField('Personal Contact Email')
    # , validators=[DataRequired(), Email()])
    idnumber = StringField('ID Number')
    cmpdname = StringField('Compound Name')
    cas = StringField('CAS')
    price = StringField('Price')
    submit = SubmitField('Save')

