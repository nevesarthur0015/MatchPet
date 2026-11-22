from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, MultipleFileField
from flask_wtf.file import FileField, MultipleFileField
from wtforms.validators import DataRequired

#Formulário de adicionar o animal
class FormAnimal(FlaskForm):
    nome= StringField('Nome:', validators=[DataRequired()])
    idade = StringField('Idade:', validators=[DataRequired()])
    raca = StringField('Raça / Tipo de animal:', validators=[DataRequired()])
    foto_principal = FileField('Foto Principal:', validators=[DataRequired()])
    fotos_extras = MultipleFileField('Fotos extras:')
    mensagem = StringField('Mensagem do doador:' , default='Procuro um novo lar para este animal')
    sexo = StringField('Sexo:' , validators=[DataRequired()])
    botao_confirmacao= SubmitField('Enviar')
    tipo = HiddenField()
# Campo oculto que permite transportar o tipo do animal recebido pela URL (GET)
# durante o envio do formulário (POST).
    