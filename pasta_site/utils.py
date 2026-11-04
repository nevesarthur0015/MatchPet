import csv
import os
from pasta_site.forms import FormAnimal
from werkzeug.utils import secure_filename
from flask import current_app

# Onde ficarão funções auxiliares que poderão ser reutilizadas futuramente.

def ler_csv (csv_file:str):
    try:
        with open(csv_file,"r",newline="",encoding="utf-8") as arquivo:       
            leitor= csv.DictReader(arquivo)
            animais = list(leitor)
            
        return animais
    except FileNotFoundError:
        return []
    

# Cria um diretório dentro de "imagens/", cujo nome é o id de um pet, ao adicioná-lo para doação. Contém as imagens do pet.
def upload_img(pet_id):
    form_animal = FormAnimal()
    pasta_pet = os.path.join('pasta_site', 'static', 'imagens', str(pet_id)) # Diretório onde as fotos vão ficar guardadas, serve pro windows
    os.makedirs(pasta_pet, exist_ok=True) # Cria o diretório
    
    pasta_base = os.path.join('imagens', str(pet_id)).replace('\\', '/') # Diretório que vai ser retornado pela função, serve pro https
    
    foto_principal = form_animal.foto_principal.data
    nome_secure = secure_filename(foto_principal.filename)
    extensao = os.path.splitext(nome_secure)[1] # Guarda se é png, jpeg...
    caminho_principal = os.path.join(pasta_pet, f"foto_principal{extensao}") # path da foto principal, usado pela linha logo abaixo
    foto_principal.save(caminho_principal) # Salva a imagem no caminho criado
    
    fotos_extras = form_animal.fotos_extras.data
    
    for i, foto in enumerate(fotos_extras, start=1):
        nome_secure = secure_filename(foto.filename)
        extensao = os.path.splitext(nome_secure)[1]
        
        # Cria o nome pras imagens extras
        nome_secure = f'extra_{i:02d}{extensao}'
        
        # path completo pras imagens. Usado na linha abaixo
        path = os.path.join(pasta_pet, nome_secure)
        
        # Salva a imagem no path criado
        foto.save(path)
        
    return pasta_base
        

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