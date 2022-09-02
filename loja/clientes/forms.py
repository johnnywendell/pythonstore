from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, validators, PasswordField, SubmitField, ValidationError
from flask_wtf import FlaskForm
from .model import Cadastrar


class CadastroClienteForm(Form):
    name = StringField('Nome: ')
    username = StringField('Usuario: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.DataRequired()])
    password = PasswordField('Senha: ', [validators.DataRequired(),validators.EqualTo('confirm', message='AS DUAS SENHAS DEVEM SER IGUAIS')])
    confirm = PasswordField('Redigite a Senha: ', [validators.DataRequired()])
    country = StringField('Pais: ', [validators.DataRequired()])
    state = StringField('Estado: ', [validators.DataRequired()])
    city = StringField('cidade: ', [validators.DataRequired()])
    contact = StringField('Contato: ', [validators.DataRequired()])
    address = StringField('Endereco: ', [validators.DataRequired()])
    zipcode = StringField('Caixa-Postal: ', [validators.DataRequired()])
    profile = FileField('Perfil: ', validators=[FileAllowed(['jpg','png', 'gif','jpeg'])])
    submit = SubmitField('Cadastrar')

    def validate_username(self, username):
        if Cadastrar.query.filter_by(username=username.data).first():
            raise ValidationError("ja existe")
    def validate_email(self, email):
        if Cadastrar.query.filter_by(email=email.data).first():
            raise ValidationError("ja existe")


class ClienteLoginForm(Form):
    email = StringField('Email: ', [validators.DataRequired()])
    password = PasswordField('Senha: ', [validators.DataRequired()])

