from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

database = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()