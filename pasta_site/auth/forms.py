#Criar os formularios do site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


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