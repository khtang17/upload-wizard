from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email


class CompanyForm(FlaskForm):
    id = HiddenField('Company ID')
    name = StringField('Company Name', validators=[DataRequired()])
    description = StringField('Company Description', validators=[DataRequired()])
    address = StringField('Company Address', validators=[DataRequired()])
    telephone_number = StringField('Telephone Number', validators=[DataRequired()])
    toll_free_number = StringField('Toll Free Number')
    fax_number = StringField('Fax Number')
    website = StringField('Website')
    sales_email = StringField('Sales Email', validators=[DataRequired(), Email()])
    personal_contact_name = StringField('Personal Contact name')
    personal_contact_email = StringField('Personal Contact Email', validators=[Email()])
    idnumber = StringField('ID Number')
    cmpdname = StringField('Compound Name')
    cas = StringField('CAS')
    price = StringField('Price')
    submit = SubmitField('Save')

