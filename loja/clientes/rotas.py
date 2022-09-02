from http.client import ImproperConnectionState
from re import sub
from flask import redirect, render_template, url_for, flash, request, session, current_app, make_response
from loja import db, app, photos, bcrypt, login_manager
from .forms import CadastroClienteForm, ClienteLoginForm
import secrets, os
from .model import Cadastrar, ClientePedido
from flask_login import login_required, current_user, login_user, logout_user
import pdfkit

@app.route('/cliente/cadastrar', methods=['GET', 'POST'])
def cadastrar_clientes():
    form = CadastroClienteForm(request.form)
    #if request.method == 'POST' and form.validate():
    #if form.validate_on_submit():
    if request.method == 'POST': # Esse funciona
        hash_password = bcrypt.generate_password_hash(form.password.data)
        cadastrar = Cadastrar(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password,
        country=form.country.data, city=form.city.data, address=form.address.data, contact=form.contact.data, zipcode=form.zipcode.data)
        db.session.add(cadastrar)
        db.session.commit()
        flash(f' OBRIGADO {form.name.data} POR SE CADASTRAR', 'success')
        return redirect(url_for('login'))
    return render_template('cliente/cliente.html', form=form)

@app.route('/cliente/login', methods=['GET', 'POST'])
def clienteLogin():
    form = ClienteLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Cadastrar.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f' Login efetuado com sucesso!!!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash(f' Senha ou email incorretos!!', 'danger')
        return redirect(url_for('clienteLogin'))
    return render_template('cliente/logincliente.html', form=form)

@app.route('/cliente/logout')
def clienteLogout():
    logout_user()
    return redirect(url_for('clienteLogin'))

@app.route('/pedido_order')
@login_required
def pedido_order():
    if current_user.is_authenticated:
        cliente_id = current_user.id
        notafiscal = secrets.token_hex(5)
        try:
            p_order = ClientePedido(notafiscal=notafiscal, cliente_id=cliente_id, pedido=session['LojainCarrinho'])
            db.session.add(p_order)
            db.session.commit()
            session.pop('LojainCarrinho')
            flash(f' Seu pedido foi Efetuado com sucesso!!', 'success')
            return redirect(url_for('pedidos', notafiscal=notafiscal))
        except Exception as e:
            print(e)
            flash(f' Nao foi possivel processar seu pedido', 'danger')
            return redirect(url_for('getcart'))
    
@app.route('/pedidos/<notafiscal>')
@login_required
def pedidos(notafiscal):
    if current_user.is_authenticated:
        gTotal = 0
        subtotal = 0 
        cliente_id = current_user.id
        cliente = Cadastrar.query.filter_by(id=cliente_id).first()
        pedidos = ClientePedido.query.filter_by(cliente_id=cliente_id, notafiscal=notafiscal).order_by(ClientePedido.id.desc()).first()
        for _key, produto in pedidos.pedido.items():
            discount = (produto['Desconto']/100) * float(produto['Preco']) * int(produto['Quantidade'])
            subtotal += float(produto['Preco']) * int(produto['Quantidade'])
            subtotal -= discount
            imposto = ("%0.2f"% (.06 * float(subtotal)))
            gTotal = float("%.2f" % float(1.06 * subtotal))
    else:
        return redirect(url_for('clienteLogin'))
    return render_template('cliente/pedido.html', notafiscal=notafiscal, imposto=imposto, subtotal=subtotal,gTotal=gTotal,cliente=cliente,pedidos=pedidos)

@app.route('/get_pdf/<notafiscal>',methods=['POST'])
@login_required
def get_pdf(notafiscal):
    if current_user.is_authenticated:
        gTotal = 0
        subtotal = 0 
        cliente_id = current_user.id
        if request.method=="POST":
            cliente = Cadastrar.query.filter_by(id=cliente_id).first()
            pedidos = ClientePedido.query.filter_by(cliente_id=cliente_id, notafiscal=notafiscal).order_by(ClientePedido.id.desc()).first()
            for _key, produto in pedidos.pedido.items():
                discount = (produto['Desconto']/100) * float(produto['Preco']) * int(produto['Quantidade'])
                subtotal += float(produto['Preco']) * int(produto['Quantidade'])
                subtotal -= discount
                imposto = ("%0.2f"% (.06 * float(subtotal)))
                gTotal = float("%.2f" % float(1.06 * subtotal))
            rendered = render_template('cliente/pdf.html', notafiscal=notafiscal, imposto=imposto, subtotal=subtotal,gTotal=gTotal,cliente=cliente,pedidos=pedidos)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type']='application/pdf'
            response.headers['content-Disposition']='inline:filename='+ notafiscal + '.pdf'
            return response
    return redirect(url_for('pedidos'))