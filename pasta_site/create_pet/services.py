from werkzeug.utils import secure_filename
from .forms import FormAnimal
import os


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