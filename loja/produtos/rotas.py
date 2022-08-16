from flask import redirect, render_template, url_for, flash, request
from loja import db, app
from loja.produtos.models import Marcas, Categorias


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