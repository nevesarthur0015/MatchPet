from . import send_email_bp
from flask import request, redirect, flash, url_for
from flask_login import login_required, current_user
from ..utils import ler_csv
from ..models import Usuario
from .email_service import mandar_email


@send_email_bp.route("/disparar_email", methods=["POST"])
@login_required
def disparar_email():
    # Lógica para disparar o email

    id_pet = request.form.get("id_pet")
    #puxa o id pet do campo hidden do form do botão
    if not id_pet:
        flash("ID do pet não encontrado","danger")
        return redirect(url_for("core.homepage_cachorro"))

    for animal in ler_csv("data/pets.csv"):
        #percorre o CSV procurando o animal com o id_pet correspondente
        if animal["id_pet"] == id_pet:

            doador = Usuario.query.get(int(animal["user_id"]))
        # pega o id do doador e procura ele no banco de dados

            if doador is None or not doador.email:
                flash("Email ou DOADOR não encontrado")
                return redirect(url_for("core.homepage_cachorro"))
            
            email_doador = doador.email
        #se achar o animal, puxa o ID e o email do doador do pet no banco de dados  
          
            email_interessado = current_user.email
        #email interessado = email do usuário logado
            nome_animal = animal["nome"] 

            try:
                mandar_email(email_doador, email_interessado, nome_animal)
                #chama func de mandar email
                print("ENVIO SMTP CONCLUIDO")
            except Exception as erro:
                flash(f"Não foi possível enviar o e-mail{erro}", "danger")
            else:
                flash("E-mail enviado com sucesso!", "success")
            return redirect(url_for("core.homepage_cachorro"))    
    else:
        flash("Animal não encontrado", "danger")
        return redirect(url_for("core.homepage_cachorro"))  