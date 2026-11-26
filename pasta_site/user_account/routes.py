from . import user_account_bp
from flask_login import current_user, login_required
from ..utils import ler_csv, dicionario_img
from flask import render_template, redirect, url_for, flash

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

@user_account_bp.route('/editar/<id_pet>')
@login_required
def editar(id_pet):
    return f"pet {id_pet} editando..."


@user_account_bp.route('/inativar/<id_pet>')
@login_required
def inativar(id_pet):

    #TODO: Função de inativar
    
    return redirect(url_for('user_account.perfil'))
    
