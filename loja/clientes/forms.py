from wsgiref.validate import validator
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, validators, PasswordField, SubmitField

class CadastroclienteForm(Form):
    name = StringField('Nome: ')
    username = StringField('Usuario: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.DataRequired()])
    password = PasswordField('Senha: ', [validators.DataRequired().validators.EqualsTo('confirm', message='AS DUAS SENHAS DEVEM SER IGUAIS')])
    confirm = PasswordField('Redigite a Senha: ', [validators.DataRequired])
    country = StringField('Pais: ', [validators.DataRequired])
    state = StringField('Estado: ', [validators.DataRequired])
    city = StringField('cidade: ', [validators.DataRequired])
    contact = StringField('Contato: ', [validators.DataRequired])
    address = StringField('Endereco: ', [validators.DataRequired])
    zipcode = StringField('Caixa-Postal: ', [validators.DataRequired])
    profile = FileField('Perfil: ', validators=[FileAllowed(['jog','png', 'gif','jpeg']), 'Apenas fotos'])
    submit = SubmitField('Cadastrar')

