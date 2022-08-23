from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField

class Addprodutos(Form):
    name = StringField('Nome :',[validators.DataRequired()])
    price = DecimalField('Preço :',[validators.DataRequired()])
    discount = IntegerField('Desconto :',[validators.DataRequired()])
    stock = IntegerField('Estoque :',[validators.DataRequired()])
    discription = TextAreaField('Descricao :',[validators.DataRequired()])
    colors = TextAreaField('Cor :',[validators.DataRequired()])
    
    image_1 = FileField('Image 1 :', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image_2 = FileField('Image 2 :', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image_3 = FileField('Image 3 :', validators=[FileAllowed(['jpg','png','gif','jpeg'])])