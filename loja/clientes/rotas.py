from flask import redirect, render_template, url_for, flash, request, session, current_app
from loja import db, app, photos
from .forms import CadastroclienteForm
import secrets, os


@app.route('/cliente/cadastrar', methods=["POST","GET"])
def cadastrar_clientes():
    form=CadastroclienteForm(request.form)
    return render_template('cliente/cliente.html')



@app.route('/addcart', methods=["POST","GET"])
def addCart():
    pass