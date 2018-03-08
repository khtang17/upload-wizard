from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.data.models.user import UserModel


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    company_name = StringField('Company Name', validators=[DataRequired()])
    company_description = StringField('Company Description', validators=[DataRequired()])
    company_address = StringField('Company Address', validators=[DataRequired()])
    company_telephone_number = StringField('Telephone Number', validators=[DataRequired()])
    company_toll_free_number = StringField('Toll Free Number')
    company_fax_number = StringField('Fax Number')
    company_website = StringField('Website')
    company_email = StringField('Company Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = UserModel.find_by_username(username.data)
        if user is not None:
            raise ValidationError('Please use different username.')

    def validate_email(self, email):
        user = UserModel.find_by_email(email.data)
        if user is not None:
            raise ValidationError('Please use different email address.')


