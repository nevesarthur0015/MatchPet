from flask import render_template,url_for,redirect,flash

from pasta_site import app, database, bcrypt

from flask_login import login_required, login_user, logout_user, current_user

from pasta_site.forms import FormLogin, FormCriarConta, FormFoto

from pasta_site.models import Usuario, Foto

import os
from werkzeug.utils import secure_filename

@app.route('/', methods=['GET','POST'])
def homepage():
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
            return redirect (url_for('perfil', id_usuario= usuario.id, usuario=usuario))
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


#Esse "<usuario>"" significa que é uma variável
#Esse "@"login_required" significa que a função perfil só pode ser acessada se o login for realizado
@app.route('/perfil/<id_usuario>',methods=['GET','POST'])
@login_required
def perfil(id_usuario): 
    #Compara o ID da URL com o ID do usuário logado
    if int(id_usuario) == int(current_user.id):
        #o usuario tá vendo o perfil dele e envia as informações do próprio usuário logado
        #O formulário de enviar foto só fica disponível se o perfil que estiver vendo for o perfil logado
        Form_Foto= FormFoto()
        if Form_Foto.validate_on_submit():
            #Essa variável arquivo recebe o arquivo da foto
            arquivo = Form_Foto.foto.data
            #Esse nome seguro é a transformação do nome do arquivo da foto para um nome que não pode bugar o sistema
            nome_seguro = secure_filename(arquivo.filename)
            #Salvar o arquivo da foto na pasta fotos_post
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            #Registrar esse arquivo no banco de dados
            foto = Foto(foto= nome_seguro, id_usuario = current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template('perfil.html', usuario=current_user, form= Form_Foto)
    else:      
        #O usuario logado tá vendo o perfil de outra pessoa e realiza uma consulta para ver qual usuario é dono daquele ID
        usuario = Usuario.query.get(int(id_usuario))
        #Se o perfil que estiver sendo visualizado não for o perfil logado, não tem formulário
        return render_template('perfil.html', usuario = usuario, form= None)


@app.route('/feed')
@login_required
def feed():
    fotos= Foto.query.order_by(Foto.data_criacao).all()
    return render_template('feed.html', fotos= fotos)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

