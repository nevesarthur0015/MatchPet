from pasta_site import database, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id= database.Column(database.Integer, primary_key=True)
    username= database.Column(database.String, nullable=False)
    senha= database.Column(database.String, nullable=False)
    email= database.Column(database.String, unique=True, nullable=False)
    fotos= database.relationship('Foto', backref='usuario',lazy=True)

class Foto(database.Model):
    id= database.Column(database.Integer, primary_key=True)
    foto= database.Column(database.String,default='default.png' )
    id_usuario= database.Column(database.Integer, database.ForeignKey('usuario.id'),nullable=False)

