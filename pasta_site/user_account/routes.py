from . import user_account_bp
from .services import salvar_alteracao
from flask_login import current_user, login_required
from ..utils import ler_csv, dicionario_img, upload_img
from .services import deletar_arquivos
from ..forms import FormAnimal
from flask import render_template, redirect, url_for, request

#A rota funciona tanto passando o usuário na URL como sem passar
@user_account_bp.route('/perfil')
@user_account_bp.route('/perfil/<usuario>')
@login_required
def perfil(usuario = None):
    usuario = current_user # O usuário será sempre aquele autenticado na requisição atual.
    pets_doados = ler_csv("data/pets.csv")
    pets_doados = [animal for animal in pets_doados if animal['user_id'] == str(usuario.id)] # Não reconhece se o id for INT!!
    
    pet_imagens = dicionario_img(pets_doados)

    return  render_template("perfil.html", usuario=usuario, pets_doados=pets_doados, pet_imagens=pet_imagens)

@user_account_bp.route('/editar/<id_pet>', methods=["GET", "POST"])
@login_required
def editar(id_pet):
    pets = ler_csv("data/pets.csv")
    pet = next((pet for pet in pets if pet['id_pet'] == id_pet), None)
    if pet == None:
        return "Animal não encontrado!"
    form_animal = FormAnimal()
        
    
    if form_animal.validate_on_submit():
        encontrado = False
        pet['nome'] = form_animal.nome.data
        pet['idade'] = form_animal.idade.data
        pet['sexo'] = form_animal.sexo.data
        pet['raca'] = form_animal.raca.data
        pet['mensagem'] = form_animal.mensagem.data
        
        deletar_arquivos(id_pet) # Deleta >>>TODOS<<< os arquivos atuais na pasta do pet.
        
        pet['imagens'] = upload_img(id_pet) # Coloca os novos arquivos na mesma pasta
        encontrado = True
    
        if not encontrado:
            return "Animal não encontrado!"
        
        salvar_alteracao(pets)
        return redirect(url_for('user_account.perfil'))
    
    return render_template("editar.html", pet=pet, form=form_animal)


@user_account_bp.route('/inativar/<id_pet>')
@login_required
def inativar(id_pet):

    #TODO: Função de inativar
    
    return redirect(url_for('user_account.perfil'))
    
