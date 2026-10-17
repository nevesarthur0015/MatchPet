from flask import render_template,url_for,redirect,flash

from pasta_site import app, database, bcrypt

from flask_login import login_required, login_user, logout_user, current_user

from pasta_site.forms import FormLogin, FormCriarConta, FormFoto

from pasta_site.models import Usuario, Foto

import os
from werkzeug.utils import secure_filename

@app.route('/', methods=['GET','POST'])
def telalogin():
    formlogin = FormLogin()
    #Esse formlogin.validate_on_submit() verifica se o formulário foi enviado via post e se atende às regras
    if formlogin.validate_on_submit():
        #Nesse query, busca no banco de dados o primeiro usuario com o e-mail digitado
        usuario= Usuario.query.filter_by(email=formlogin.email.data).first()
        #Se não achar um usuário, dispara um flash com a mensagem "usuário não cadastrado" e a categoria é "erro"
        if not usuario:
            flash("Usuário não cadastrado", 'erro')
        #Se achar o usuário mas senha digitada no 'formlogin.senha.data' não for igual a senha do usuario 'usuario.senha', dispara um flash com a mensagem 'Senha incorreta. Tente novamente' e a categoria é 'erro'
        elif not bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            flash("Senha incorreta. Tente novamente", 'erro')
        #Esse "if usuario" é se tiver achado e esse outro que tem bcrypt compara a senha do usuario "usuario.senha" com o senha digitada "formlogin.senha.data"
        if usuario and bcrypt.check_password_hash(usuario.senha,formlogin.senha.data):
            #Se as duas condições forem atendidas, então inicia a sessao com login_user(usuario)
            login_user(usuario)
            return redirect (url_for('cachorro', id_usuario= usuario.id, usuario=usuario))
    return render_template('homepage.html', form = formlogin)

@app.route('/criarconta', methods=['GET','POST'])
def criarconta():
    formcriarconta= FormCriarConta()
    #A variável usuário busca no banco de dados algum usuario com o email digitado no formulário
    usuario= Usuario.query.filter_by(email=formcriarconta.email.data).first()
    #Se já tiver um usuário com esse email, dispara um flash
    if usuario:
        flash("Email já cadastrado. Tente fazer login",'erro')
    else:
        #Esse "formcriarconta.validate_on_submit()" é uma condição de que o formulário criar conta cumpre todas as exigências no forms.py para esse formulário específico
        if formcriarconta.validate_on_submit():
            #Essa variavel senha recebe um hash seguro. Garante que a senha não fique exposta
            senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
            #Se cumprir as exigências, cria uma variável usuário que armazena o objeto 'Usuario' que recebe username, email e senha de acordo com o formulário "formcriarconta"
            usuario = Usuario(username=formcriarconta.username.data , email=formcriarconta.email.data , senha=senha )
            #Esse add e o commit salva a variavel usuario em um banco de dados
            database.session.add(usuario)
            database.session.commit()
            #O login user faz o login quando cria a conta, sem precisar fazer o login logo em seguida
            login_user(usuario, remember=True)
            #Esse return redirect redireciona a página para a função 'perfil', com a variavel 'usuario' de tal função recebendo o dado username da classe Usuario
            return redirect(url_for('homepage'))
    return render_template('criarconta.html', form = formcriarconta)



#Esse "@"login_required" significa que a função perfil só pode ser acessada se o login for realizado
@app.route('/cachorro',methods=['GET','POST'])
@login_required
def cachorro(): 
    return render_template('cachorro.html')

#Esse "@"login_required" significa que a função perfil só pode ser acessada se o login for realizado
@app.route('/gato',methods=['GET','POST'])
@login_required
def gato(): 
    return render_template('gato.html')

#Esse "@"login_required" significa que a função perfil só pode ser acessada se o login for realizado
@app.route('/outros',methods=['GET','POST'])
@login_required
def outros(): 
    return render_template('outros.html')

#Esse "@"login_required" significa que a função perfil só pode ser acessada se o login for realizado
@app.route('/adicionar',methods=['GET','POST'])
@login_required
def adicionar(): 
    return render_template('adicionar.html')



@app.route('/feed')
@login_required
def feed():
    fotos= Foto.query.order_by(Foto.data_criacao).all()
    return render_template('feed.html', fotos= fotos)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('telalogin'))

