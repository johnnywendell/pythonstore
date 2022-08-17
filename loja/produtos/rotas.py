from flask import redirect, render_template, url_for, flash, request, session
from loja import db, app, photos
from loja.produtos.models import Marcas, Categorias, Addproduto
from .forms import Addprodutos
import secrets

@app.route('/addmarca', methods=['GET','POST'])
def addmarca():
    if 'email' not in session:
        flash(f'favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        getmarca = request.form.get('marca')
        marca = Marcas(name=getmarca)
        db.session.add(marca)
        db.session.commit()
        flash(f'A marca {getmarca} foi cadastrada com sucesso', 'success')
        return redirect(url_for('addmarca'))
    return render_template('produtos/addmarca.html', marcas='marcas')

@app.route('/updatemarca/<int:id>', methods=['GET','POST'])
def updatemarcas(id):
    if 'email' not in session:
        flash(f'favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))
    updatemarca = Marcas.query.get_or_404(id)
    marca = request.form.get('marca')
    if request.method =='POST':
        updatemarca.name = marca
        db.session.commit()
        flash(f'Seu fabricante foi atualizado com sucesso!!', 'success')
        return redirect(url_for('marcas'))
    return render_template('produtos/updatemarca.html', title="Atualizar Fabricantes", updatemarca=updatemarca)

@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash(f'favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        getmarca = request.form.get('categoria')
        cat = Categorias(name=getmarca)
        db.session.add(cat)
        db.session.commit()
        flash(f'A Categoria {getmarca} foi cadastrada com sucesso', 'success')
        return redirect(url_for('addcat'))
    return render_template('produtos/addmarca.html')

@app.route('/updatecat/<int:id>', methods=['GET','POST'])
def updatecats(id):
    if 'email' not in session:
        flash(f'favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))
    updatecat = Categorias.query.get_or_404(id)
    categoria = request.form.get('categoria')
    if request.method =='POST':
        updatecat.name = categoria
        db.session.commit()
        flash(f'Sua categoria foi atualizada com sucesso!!', 'success')
        return redirect(url_for('categorias'))
    return render_template('produtos/updatemarca.html', title="Atualizar Categorias", updatecat=updatecat)

@app.route('/addproduto', methods=['GET','POST'])
def addproduto():
    if 'email' not in session:
        flash(f'favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))

    marcas = Marcas.query.all()
    categorias = Categorias.query.all()
    form = Addprodutos(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        marca = request.form.get('marca')
        categoria = request.form.get('categoria')
        image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
        image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
        image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
        addprod = Addproduto(name=name, price=price, discount=discount,stock=stock,colors=colors,desc=desc, marca_id=marca,categoria_id=categoria,
        image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(addprod)
        db.session.commit()
        flash(f'Produto {name} foi cadastrado com sucesso', 'success')
        return redirect(url_for('admin'))

    return render_template('produtos/addproduto.html', title='Cadastrar Produtos',form=form ,marcas = marcas,categorias = categorias)