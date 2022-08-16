from flask import redirect, render_template, url_for, flash, request
from loja import db, app, photos
from loja.produtos.models import Marcas, Categorias
from .forms import Addprodutos

@app.route('/addmarca', methods=['GET','POST'])
def addmarca():
    if request.method == "POST":
        getmarca = request.form.get('marca')
        marca = Marcas(name=getmarca)
        db.session.add(marca)
        db.session.commit()
        flash(f'A marca {getmarca} foi cadastrada com sucesso', 'success')
        return redirect(url_for('addmarca'))

    return render_template('produtos/addmarca.html', marcas='marcas')

@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if request.method == "POST":
        getmarca = request.form.get('categoria')
        cat = Categorias(name=getmarca)
        db.session.add(cat)
        db.session.commit()
        flash(f'A Categoria {getmarca} foi cadastrada com sucesso', 'success')
        return redirect(url_for('addcat'))

    return render_template('produtos/addmarca.html')

@app.route('/addproduto', methods=['GET','POST'])
def addproduto():
    marcas = Marcas.query.all()
    categorias = Categorias.query.all()
    form = Addprodutos(request.form)
    if request.method == "POST":
        photos.save(request.files.get('image_1'))
        photos.save(request.files.get('image_2'))
        photos.save(request.files.get('image_3'))

    return render_template('produtos/addproduto.html', title='Cadastrar Produtos',form=form ,marcas = marcas,categorias = categorias)