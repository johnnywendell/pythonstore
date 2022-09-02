from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError
from.models import User

class RegistrationForm(Form):
    name = StringField('Nome', [validators.Length(min=4, max=25)])
    username = StringField('Usuario', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Digite Sua Senha', [validators.DataRequired()])

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("ja existe")
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("ja existe")

class LoginForms(Form):
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Digite Sua Senha', [validators.DataRequired()])
