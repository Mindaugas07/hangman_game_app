from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed
from app.models.user_auth.user_auth import GameUser


class RegistrationForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    email = StringField("E-mail", [Email()])
    password = PasswordField("Password", [DataRequired()])
    confirmed_password = PasswordField(
        "Please repeat the password", [EqualTo("password", "Password must match.")]
    )
    submit = SubmitField("Register")

    # def check_username(self, name):
    #     unique_user = GameUser.query.filter_by(name=name.data).first()
    #     if unique_user:
    #         raise ValidationError(
    #             "This username is already taken. Please use another one."
    #         )

    # def check_email(self, email):
    #     new_user = GameUser.query.filter_by(email=email.data).first()
    #     if new_user:
    #         raise ValidationError(
    #             "This e-mail is already taken. Please use another one."
    #         )


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
