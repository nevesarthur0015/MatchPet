from ..forms import FormAnimal
from . import create_pet_bp
from ..utils import upload_img
from flask import request, redirect, flash, url_for, render_template
from flask_login import login_required, current_user
import csv
import uuid


#Esse "@"login_required" significa que a função categoria só pode ser acessada se o login for realizado
@create_pet_bp.route('/categoria',methods=['GET','POST'])
@login_required
def categoria(): 
    return render_template('categoria.html')

@create_pet_bp.route('/adicionar', methods=['GET','POST'])
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
           return redirect(url_for("core.homepage_cachorro"))
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

       return redirect(url_for('core.homepage_cachorro'))

    return render_template('adicionar1.html', form=form_animal)