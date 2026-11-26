from flask import Flask
from .extensions import mail, bcrypt, database, login_manager
from dotenv import load_dotenv


import os

load_dotenv()

def create_app():
    
    app = Flask(__name__)

    #config SMTP
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "a208c85e") # Tenta resgatar a secret_key do .env, se nn conseguir, usa a segunda
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['UPLOAD_FOLDER'] = 'pasta_site/static/'

    database.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    #Esse login_manager.login_view indica para qual página o usuário deve ser direcionado caso tente acessar um página protegida sem estar logado, isto é, o que tem @login_required. Nesse caso, será direcionado para a rota com a função "homepage"
    login_manager.login_view = 'auth.telalogin'

    #Mensagem que aparece quando tenta acessar uma página que tem @login_required quando não está logado
    login_manager.login_message = 'Faça login para acessar esta página'

    # Importa e registra todos os blueprints
    from pasta_site.core import core_bp
    from pasta_site.auth import auth_bp
    from pasta_site.create_pet import create_pet_bp
    from pasta_site.send_email import send_email_bp
    from pasta_site.user_account import user_account_bp

    app.register_blueprint(core_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(create_pet_bp, url_prefix="/create-pet")
    app.register_blueprint(user_account_bp, url_prefix="/user")
    app.register_blueprint(send_email_bp)


<<<<<<< HEAD
    #Não salva em cache as rotas que tem @login_required, por isso não é possível voltar para uma página protegida apertando na seta de voltar após realizar logout
    @app.after_request
    def add_header(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
=======
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'pasta_site/static/'
>>>>>>> 628f878677e5c16d477ecf71b4a904afac7e6111

    return app

<<<<<<< HEAD
=======

#Não salva em cache as rotas que tem @login_required, por isso não é possível voltar para uma página protegida apertando na seta de voltar após realizar logout
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


database= SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  

#Esse login_manager.login_view indica para qual página o usuário deve ser direcionado caso tente acessar um página protegida sem estar logado, isto é, o que tem @login_required. Nesse caso, será direcionado para a rota com a função "homepage"
login_manager.login_view = 'telalogin'

#Mensagem que aparece quando tenta acessar uma página que tem @login_required quando não está logado
login_manager.login_message = 'Faça login para acessar esta página'

from pasta_site import routes
>>>>>>> 628f878677e5c16d477ecf71b4a904afac7e6111
