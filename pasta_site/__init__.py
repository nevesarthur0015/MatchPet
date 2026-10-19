from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = '21072006'
app.config['UPLOAD_FOLDER'] = 'static/fotos_posts'



#Não salva em cache as rotas que tem @login_required, por isso não é possível voltar para um apagina protegida apertando na seta de voltar após realizar logout
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


database= SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.config['SECRET_KEY'] = 'chave_secreta'

#Esse login_manager.login_view indica para qual página o usuário deve ser direcionado caso tente acessar um página protegida sem estar logado, isto é, o que tem @login_required. Nesse caso, será direcionado para a rota com a função "homepage"
login_manager.login_view = 'telalogin'

#Mensagem que aparece quando tenta acessar uma página que tem @login_required quando não está logado
login_manager.login_message = 'Faça login para acessar esta página'

from pasta_site import routes