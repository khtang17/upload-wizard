from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email
from flask_wtf.file import FileField, FileAllowed
from flask_user import UserManager
from flask_user.forms import RegisterForm

class CustomRegistrationForm(RegisterForm):
    user_info = TextAreaField(validators=[DataRequired()], render_kw={"placeholder" : "Tell us brielf about you and your company"})


class CustomUserManager(UserManager):
    def customize(self, app):
        self.RegisterFormClass = CustomRegistrationForm
