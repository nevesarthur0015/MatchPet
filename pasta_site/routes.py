import os

from flask import render_template,url_for,redirect,flash,request

from pasta_site import app, database, bcrypt

from flask_login import login_required, login_user, logout_user, current_user

from pasta_site.forms import FormLogin, FormCriarConta, FormAnimal

from pasta_site.models import Usuario, Foto

from werkzeug.utils import secure_filename

import uuid

import csv

from pasta_site.utils import ler_csv, upload_img, dicionario_img

from .email_service import mandar_email

@app.route('/')
def homepage_cachorro():
#função pra ler csv passando o arquivo como parâmetro
    dados_animais = ler_csv("data/pets.csv")
    pet_imagens = dicionario_img(dados_animais)
    dados_animais = [animal for animal in dados_animais if animal["tipo"] == "cachorro"]
    # Percorre a lista de animais e verifica o tipo
    # de cada um, adicionando à nova lista apenas os cachorros.
    
    
     
    return render_template('homepages/homepage_cachorro.html',dados_animais = dados_animais, pet_imagens = pet_imagens) 
    #Agora so adicionar o for no html 

@app.route('/gato')
def homepage_gato():
    dados_animais = ler_csv("data/pets.csv")
    pet_imagens = dicionario_img(dados_animais)
    dados_animais = [animal for animal in dados_animais if animal["tipo"] == "gato"]
    # Percorre a lista de animais e verifica o tipo
    # de cada um, adicionando à nova lista apenas os gatos.
         
    return render_template('homepages/homepage_gato.html',dados_animais = dados_animais, pet_imagens = pet_imagens) 
    #Agora so adicionar o for no html

@app.route('/outros')
def homepage_outros():
    dados_animais = ler_csv("data/pets.csv")
    pet_imagens = dicionario_img(dados_animais)
    dados_animais = [animal for animal in dados_animais if animal["tipo"] == "outros"]
    # Percorre a lista de animais e verifica o tipo
    # de cada um, adicionando à nova lista apenas os ""outros"".
             
    return render_template('homepages/homepage_outros.html',dados_animais = dados_animais, pet_imagens = pet_imagens) 
    #Agora so adicionar o for no html

@app.route('/telalogin', methods=['GET','POST'])
def telalogin():
    formlogin = FormLogin()
    
    # Esse formlogin.validate_on_submit() verifica se o formulário foi enviado via post e se atende às regras
    if formlogin.validate_on_submit():
        # Nesse query, busca no banco de dados o primeiro usuario com o e-mail digitado
        usuario= Usuario.query.filter_by(email=formlogin.email.data).first()
        
        # Se não achar um usuário, dispara um flash com a mensagem "usuário não cadastrado" e a categoria é "erro"
        if not usuario:
            flash("Usuário não cadastrado", 'erro')
            
        # Se achar o usuário mas senha digitada no 'formlogin.senha.data' não for igual a senha do usuario 'usuario.senha', 
        # dispara um flash com a mensagem 'Senha incorreta. Tente novamente' e a categoria é 'erro'
        elif not bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            flash("Senha incorreta. Tente novamente", 'erro')
            
        #Esse "if usuario" é se tiver achado e esse outro que tem bcrypt compara a senha do usuario "usuario.senha" 
        # com o senha digitada "formlogin.senha.data"
        if usuario and bcrypt.check_password_hash(usuario.senha,formlogin.senha.data):  # inicia a sessao com login_user(usuario)
            login_user(usuario)
            return redirect (url_for('homepage_cachorro', id_usuario= usuario.id, usuario=usuario))
        
    return render_template('login.html', form = formlogin)

@app.route('/criarconta', methods=['GET','POST'])
def criarconta():
    formcriarconta= FormCriarConta()
    # A variável usuário busca no banco de dados algum usuario com o email digitado no formulário
    usuario= Usuario.query.filter_by(email=formcriarconta.email.data).first()
    # Se já tiver um usuário com esse email, dispara um flash
    if usuario:
        flash("Email já cadastrado. Tente fazer login",'erro')
    else:
        # Esse "formcriarconta.validate_on_submit()" é uma condição de que o formulário criar conta cumpre todas 
        # as exigências no forms.py para esse formulário específico
        if formcriarconta.validate_on_submit():
            # Essa variavel senha recebe um hash seguro. Garante que a senha não fique exposta
            senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
            # Se cumprir as exigências, cria uma variável usuário que armazena o objeto 'Usuario' que recebe username, 
            # email e senha de acordo com o formulário "formcriarconta"
            usuario = Usuario(username=formcriarconta.username.data , email=formcriarconta.email.data , senha=senha )
            #Esse add e o commit salva a variavel usuario em um banco de dados
            database.session.add(usuario)
            database.session.commit()
            #O login user faz o login quando cria a conta, sem precisar fazer o login logo em seguida
            login_user(usuario, remember=True)
            #Esse return redirect redireciona a página para a função 'perfil', com a variavel 'usuario' de tal 
            #função recebendo o dado username da classe Usuario
            return redirect(url_for('homepage_cachorro'))
    return render_template('criarconta.html', form = formcriarconta)


#Esse "@"login_required" significa que a função categoria só pode ser acessada se o login for realizado
@app.route('/categoria',methods=['GET','POST'])
@login_required
def categoria(): 
    return render_template('categoria.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('telalogin'))

@app.route('/adicionar', methods=['GET','POST'])
@login_required
def adicionar():
    form_animal= FormAnimal()
    if request.method == "GET":
               form_animal.tipo.data = request.args.get("tipo")
    # Recupera o parâmetro da URL (GET) e preenche o campo oculto do formulário.           
    if form_animal.validate_on_submit():
       
        #Se o form passar na validação ele puxa os dados do form pra mandar pro CSV
       tipo = form_animal.tipo.data 
       tipos_validos = ["cachorro","gato","outros"] 

       if tipo not in tipos_validos:
           flash ("categoria de animal inválida","danger" )
           return redirect(url_for("homepage_cachorro"))
       #Validação: se o usuário informar um tipo inválido pela URL ou alterar o campo oculto pelo DevTools,
       #O sistema bloqueia o cadastro, exibe uma mensagem de erro e redireciona o usuário para a página inicial.
       
       nome_pet = form_animal.nome.data
       idade_pet = form_animal.idade.data
       sexo_pet = form_animal.sexo.data
       raca_pet = form_animal.raca.data
       pet_id = str(uuid.uuid4()) #Usa o UUID que gera um ID único para cada pet 
       imagens_pet = upload_img(pet_id)
       mensagem_pet = form_animal.mensagem.data
       user_id = current_user.id
       
       with open("data/pets.csv","a",newline = "",encoding="utf-8") as arquivo:
           escritor = csv.writer(arquivo)
           escritor.writerow([nome_pet,idade_pet,sexo_pet,raca_pet,mensagem_pet,pet_id,user_id,tipo, imagens_pet]) 
           # abre o arquivo CSV, e grava os dados enviados no form (Menos imagem por enquanto)

       return redirect(url_for('homepage_cachorro'))
    flash ("categoria de animal inválida","danger" )
    return render_template('adicionar1.html', form=form_animal)

@app.route('/detalhes/<id_pet>')
def detalhes(id_pet):
    dados_animais = ler_csv("data/pets.csv")
    dados_animal = [animal for animal in dados_animais if animal["id_pet"] == id_pet]
    #percorre o csv e cria uma lista com os dados do pet recebido após achar
    if not dados_animal:
        return "Animal não encontrado", 404
    #se não tiver esse animal cadastrado da esse erro

    
    pet_imagens = dicionario_img(dados_animal)
    return render_template('detalhes.html', dados_animal = dados_animal, pet_imagens = pet_imagens)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

#A rota funciona tanto passando o usuário na URL como sem passar
@app.route('/perfil')
@app.route('/perfil/<usuario>')
@login_required
def perfil(usuario = None):
   usuario = current_user
# O usuário será sempre aquele autenticado na requisição atual.

   return  f"<p>HTML {current_user.username}</p>"
#Agora é so criar o HTML e passar o template e a var de usuário


@app.route("/disparar_email", methods=["POST"])
@login_required
def disparar_email():
    # Lógica para disparar o email

    id_pet = request.form.get("id_pet")
    #puxa o id pet do campo hidden do form do botão
    if not id_pet:
        flash("ID do pet não encontrado","danger")
        return redirect(url_for("homepage_cachorro"))

    for animal in ler_csv("data/pets.csv"):
        #percorre o CSV procurando o animal com o id_pet correspondente
        if animal["id_pet"] == id_pet:

            doador = Usuario.query.get(int(animal["user_id"]))
        # pega o id do doador e procura ele no banco de dados

            if doador is None or not doador.email:
                flash("Email ou DOADOR não encontrado")
                return redirect(url_for("homepage_cachorro"))
            
            email_doador = doador.email
        #se achar o animal, puxa o ID e o email do doador do pet no banco de dados  
          
            email_interessado = current_user.email
        #email interessado = email do usuário logado
            nome_animal = animal["nome"] 

            try:
                mandar_email(email_doador, email_interessado, nome_animal)
                #chama func de mandar email
            except Exception:
                flash("Não foi possível enviar o e-mail", "danger")
            else:
                flash("E-mail enviado com sucesso!", "success")
            return redirect(url_for("homepage_cachorro"))    
    else:
        flash("Animal não encontrado", "danger")
        return redirect(url_for("homepage_cachorro"))  
    