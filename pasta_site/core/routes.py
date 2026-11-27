from . import core_bp
from flask import render_template
from ..utils import ler_csv, dicionario_img
from flask_login import current_user

@core_bp.route('/')
def homepage_cachorro():
#função pra ler csv passando o arquivo como parâmetro
    dados_animais = ler_csv("data/pets.csv")
    dados_animais = [animal for animal in dados_animais if animal["tipo"] == "cachorro" and animal["ativo"] == '1']
    pet_imagens = dicionario_img(dados_animais)
    # Percorre a lista de animais e verifica o tipo
    # de cada um, adicionando à nova lista apenas os cachorros.
    
    
     
    return render_template('core/homepage_cachorro.html',dados_animais = dados_animais, pet_imagens = pet_imagens) 
    #Agora so adicionar o for no html 

@core_bp.route('/gato')
def homepage_gato():
    dados_animais = ler_csv("data/pets.csv")
    dados_animais = [animal for animal in dados_animais if animal["tipo"] == "gato" and animal["ativo"] == '1']
    pet_imagens = dicionario_img(dados_animais)
    # Percorre a lista de animais e verifica o tipo
    # de cada um, adicionando à nova lista apenas os gatos.
         
    return render_template('core/homepage_gato.html',dados_animais = dados_animais, pet_imagens = pet_imagens) 
    #Agora so adicionar o for no html

@core_bp.route('/outros')
def homepage_outros():
    dados_animais = ler_csv("data/pets.csv")
    dados_animais = [animal for animal in dados_animais if animal["tipo"] == "outros" and animal["ativo"] == '1'] 
    pet_imagens = dicionario_img(dados_animais)
    # Percorre a lista de animais e verifica o tipo
    # de cada um, adicionando à nova lista apenas os ""outros"".
             
    return render_template('core/homepage_outros.html',dados_animais = dados_animais, pet_imagens = pet_imagens) 
    #Agora so adicionar o for no html
  
@core_bp.route('/detalhes/<id_pet>')
def detalhes(id_pet):
    dados_animais = ler_csv("data/pets.csv")
    dados_animal = [animal for animal in dados_animais if animal["id_pet"] == id_pet]
    #percorre o csv e cria uma lista com os dados do pet recebido após achar
    if not dados_animal:
        return "Animal não encontrado", 404
    #se não tiver esse animal cadastrado da esse erro

    
    pet_imagens = dicionario_img(dados_animal)
    return render_template('core/detalhes.html', dados_animal = dados_animal, pet_imagens = pet_imagens, contato = current_user.email)

@core_bp.route('/sobre')
def sobre():
    return render_template('core/sobre.html')