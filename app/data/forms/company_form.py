from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email
from flask_wtf.file import FileField, FileAllowed


class CompanyForm(FlaskForm):
    id = HiddenField('Company ID')
    file = FileField('Company Logo:', render_kw={"class": "form-control btn btn-outline-info"},
                     validators=[
                         FileAllowed(['png', 'jpeg', 'jpg'], 'Please upload only allowed files! (.txt, .jpeg, .jpg)')
                     ])
    logo = HiddenField('Logo')
    name = StringField('Company Name: *', render_kw={"class": "form-control m-input",
                                                     "placeholder": "Enter company name"}, validators=[DataRequired()])
    description = TextAreaField('Company Description: *', render_kw={"class": "form-control",
                                                                     "id": "m_autosize_1",
                                                                     "rows": 3}, validators=[DataRequired()])
    address = TextAreaField('Company Address: *', render_kw={"class": "form-control",
                                                                      "id": "m_autosize_2",
                                                                      "rows": 3}, validators=[DataRequired()])
    telephone_number = StringField('Telephone Number: *',
                                   render_kw={"class": "form-control m-input",
                                              "placeholder": "Enter company telephone number"},
                                   validators=[DataRequired()])
    toll_free_number = StringField('Toll Free Number:',
                                   render_kw={"class": "form-control m-input",
                                              "placeholder": "Enter company toll free number"})
    fax_number = StringField('Fax Number:', render_kw={"class": "form-control m-input",
                                                       "placeholder": "Enter company fax number"})
    website = StringField('Website:', render_kw={"class": "form-control m-input",
                                                 "placeholder": "Enter company website"})
    sales_email = StringField('Sales Email:', render_kw={"class": "form-control m-input",
                                                         "placeholder": "Enter company sales email"})
    personal_contact_name = StringField('Personal Contact name:',
                                        render_kw={"class": "form-control m-input",
                                                   "placeholder": "Enter personal contact name"})
    personal_contact_email = StringField('Personal Contact Email:',
                                         render_kw={"class": "form-control m-input",
                                                    "placeholder": "Enter personal contact email"})
    # , validators=[DataRequired(), Email()])
    idnumber = StringField('ID Number:', render_kw={"class": "form-control m-input",
                                                    "placeholder": "Enter id number"})
    cmpdname = StringField('Compound Name:', render_kw={"class": "form-control m-input",
                                                        "placeholder": "Enter compound name"})
    cas = StringField('CAS:', render_kw={"class": "form-control m-input",
                                         "placeholder": "Enter cas number"})
    price = StringField('Price:', render_kw={"class": "form-control m-input",
                                             "placeholder": "Enter price"})
    submit = SubmitField('Save', render_kw={"class": "btn btn-success"})

