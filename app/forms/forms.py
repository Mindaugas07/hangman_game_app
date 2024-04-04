from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    email = StringField("E-mail", [Email()])
    password = PasswordField("Pasword", [DataRequired()])
    confirmed_password = PasswordField(
        "Please repeat the password", [EqualTo("password", "Password must match.")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("E-mail", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class AccountUpdateForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    email = StringField("E-mail", [DataRequired()])
    piture = FileField(
        "Update profile picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")
