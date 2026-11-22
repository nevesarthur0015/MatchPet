from . import user_account_bp
from flask_login import current_user, login_required

#A rota funciona tanto passando o usuário na URL como sem passar
@user_account_bp.route('/perfil')
@user_account_bp.route('/perfil/<usuario>')
@login_required
def perfil(usuario = None):
    usuario = current_user
    # O usuário será sempre aquele autenticado na requisição atual.

    return  f"<p>HTML {current_user.username}</p>"
#Agora é so criar o HTML e passar o template e a var de usuário
