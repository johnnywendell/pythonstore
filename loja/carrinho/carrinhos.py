from crypt import methods
from curses import echo
from operator import truediv
from statistics import quantiles
from flask import redirect, render_template, url_for, flash, request, session, current_app
from loja import db, app
from loja.produtos.models import Addproduto

def m_dicionarios(dic1,dic2):
    if isinstance(dic1,list) and isinstance(dic2,lis):
        return dic1 + dic2
    elif isinstance(dic1,dict) and isinstance(dic2,dict):
        return dict(list(dic1.items()) + list(dic2.items()))
    return False


@app.route('/addcart', methods=["POST"])
def addCart():
    try:
        produto_id = request.form.get('produto_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors') 
        produto = Addproduto.query.filter_by(id=produto_id).first()   
        if produto_id and quantity and colors and request.method == "POST":
            DicItems = {produto_id:{'Nome':produto.name, 'Preco': produto.price, 'Desconto': produto.discount, 'Cor': colors,
            'Quantidade':quantity, 'image':produto.image_1, 'colors':produto.colors}}
            if 'LojainCarrinho' in session:
                print(session['LojainCarrinho'])
                if produto_id in session['LojainCarrinho']:
                    if produto_id in session['LojainCarrinho']:
                        for key, item in session['LojainCarrinho'].items():
                            if int(key) == int(produto_id):
                                session.modified = True
                                item['quantity']=+1
                else:
                    session['LojainCarrinho'] = m_dicionarios(session['LojainCarrinho'],DicItems)
                    return redirect(request.referrer)
            else:
                session['LojainCarrinho'] = DicItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

    
@app.route('/carros')
def getcart():
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho']) <=0:
        return redirect(url_for('home'))
    subtotal = 0
    valorpagar = 0
    for key, produto in session['LojainCarrinho'].items():
        discount = (produto['Desconto']/100) * float(produto['Preco']) * int(produto['Quantidade'])
        subtotal += float(produto['Preco']) * int(produto['Quantidade'])
        subtotal -= discount
        imposto = ("%0.2f"% (.06 * float(subtotal)))
        valorpagar = float("%.2f" % float(1.06 * subtotal))

    return render_template('produtos/carros.html', imposto=imposto, valorpagar=valorpagar,)

@app.route('/updatecarro/<int:code>', methods=["POST"])
def updatecarro(code):
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho']) <=0:
        return redirect(url_for('home'))
    if request.method =="POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['LojainCarrinho'].items():
                if int(key) == code:
                    item['Quantidade'] = quantity
                    item['Cor'] = color
                    flash('Itens atualizados com sucesso', 'success')
                    return redirect(url_for('getcart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getcart'))

@app.route('/deletecart/<int:id>')
def deletercart(id):
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho']) <=0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['LojainCarrinho'].items():
            if int(key) == id:
                session['LojainCarrinho'].pop(key,None)
                flash('Item Excluido!!', 'success')
                return redirect(url_for('getcart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getcart'))

@app.route('/limparcarro')
def limparcarro():
    try:
        session.pop('LojainCarrinho',None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

@app.route('/logout')
def logout():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)