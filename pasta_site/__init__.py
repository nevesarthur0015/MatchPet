from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = '21072006'

database= SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

#Esse login_manager.login_view indica para qual página o usuário deve ser direcionado caso tente acessar um página protegida sem estar logado, isto é, o que tem @login_required. Nesse caso, será direcionado para a rota com a função "homepage"
login_manager.login_view = 'homepage'

from pasta_site import routes