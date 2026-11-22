import csv
import os
from flask import current_app
from wtforms.validators import ValidationError
from .models import Usuario

# Onde ficarão funções auxiliares que poderão ser reutilizadas futuramente.
def validate_email(email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado, faça login para continuar")

def ler_csv (csv_file:str):
    try:
        with open(csv_file,"r",newline="",encoding="utf-8") as arquivo:       
            leitor= csv.DictReader(arquivo)
            animais = list(leitor)
            
        return animais
    except FileNotFoundError:
        return []

def dicionario_img(dados_animais):
    pet_imagens = []
    for pet in dados_animais:
        # cria um dicionário com o id do pet, a foto principal e as fotos extras separados.
        pet_dicionario = {"id": pet['id_pet']}
        
        fotos_extras = []
        for arquivo in os.listdir(f"pasta_site/static/{pet['imagens']}"):
            if arquivo.startswith('foto_principal'):
                pet_dicionario["foto_principal"] = f"imagens/{pet['id_pet']}/{arquivo}"
            
            elif arquivo.startswith('extra_'):
                fotos_extras.append(f"imagens/{pet['id_pet']}/{arquivo}")
                
        if fotos_extras:
            pet_dicionario["fotos_extras"] = fotos_extras
        
        pet_imagens.append(pet_dicionario)
        
    return pet_imagens