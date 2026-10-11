from flask import render_template,url_for

from pasta_site import app

from flask_login import login_required

@app.route('/')
def homepage():
    return render_template('homepage.html')


#Esse "<usuario>"" significa que é uma variável
#Esse "@"login_required" significa que a função perfil só pode ser acessada se o login for realizado
@app.route('/perfil/<usuario>')
@login_required
def perfil(usuario):
    return render_template('perfil.html', usuario = usuario)
