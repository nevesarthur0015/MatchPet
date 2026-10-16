#Criar os formularios do site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from pasta_site.models import Usuario

#Esse E-mail entre parenteres é o label da variável email
class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[ DataRequired(), Email() ])
    senha = PasswordField('Senha', validators=[DataRequired()])
    botao_confirmacao = SubmitField('Fazer login')
#DataRequired serve para dizer que não aceita campo vazio
class FormCriarConta(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    username = StringField('Username', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmação de senha', validators=[DataRequired(),EqualTo('senha', message='As senhas não coincidem')])
    botao_confirmacao = SubmitField('Criar Conta')

#Formulário de enviar foto
class FormFoto(FlaskForm):
    foto = FileField('Foto', validators=[DataRequired()])
    botao_confirmacao= SubmitField('Enviar')



#Serve para analisar se o email já está cadastrado
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado, faça login para continuar")