from flask import render_template, session, request, url_for, flash, redirect, flash
from loja import app, db, bcrypt
from .formulario import RegistrationForm, LoginForms
from .models import User
import os


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))
    return render_template('admin/index.html', title='Pagina administrativa')


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data,email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Obrigado {form.name.data} por se registrar', 'success')
        return redirect(url_for('login'))
    return render_template('admin/registrar.html', form=form, title="Página de registros")



@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForms(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Ola {form.email.data} acesso liberado', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:   
            flash('NAO FOI POSSIVEL ENTRAR NO SISTEMA', 'danger')
    return render_template('admin/login.html', form=form, title='Pagina Login')

