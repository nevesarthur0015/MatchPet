from flask import render_template,url_for,redirect

from pasta_site import app, database, bcrypt

from flask_login import login_required, login_user, logout_user

from pasta_site.forms import FormLogin, FormCriarConta

from pasta_site.models import Usuario, Foto

@app.route('/', methods=['GET','POST'])
def homepage():
    formlogin = FormLogin()
    return render_template('homepage.html', form = formlogin)

@app.route('/criarconta', methods=['GET','POST'])
def criarconta():
    formcriarconta= FormCriarConta()
    #Esse "formcriarconta.validate_on_submit()" é uma condição de que o formulário criar conta cumpre todas as exigências no forms.py para esse formulário específico
    if formcriarconta.validate_on_submit():
        #Essa variavel senha recebe um hash seguro. Garante que a senha não fique exposta
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        #Se cumprir as exigências, cria uma variável usuário que armazena o objeto 'Usuario' que recebe username, email e senha de acordo com o formulário "formcriarconta"
        usuario = Usuario(username=formcriarconta.username.data , email=formcriarconta.email.data , senha=senha )
        #Esse add e o commit salva a variavel usuario em um banco de dados
        database.session.add(usuario)
        database.session.commit()
        #O login user faz o login quando cria a conta, sem precisar fazer o login logo em seguida
        login_user(usuario, remember=True)
        #Esse return redirect redireciona a página para a função 'perfil', com a variavel 'usuario' de tal função recebendo o dado username da classe Usuario
        return redirect(url_for('perfil', usuario = usuario.username))
    return render_template('criarconta.html', form = formcriarconta)


#Esse "<usuario>"" significa que é uma variável
#Esse "@"login_required" significa que a função perfil só pode ser acessada se o login for realizado
@app.route('/perfil/<usuario>')
@login_required
def perfil(usuario):
    return render_template('perfil.html', usuario = usuario)
