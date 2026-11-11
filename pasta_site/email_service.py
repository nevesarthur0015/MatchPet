from . import mail
#importa a instância de disparo de email

from flask_mail import Message


def mandar_email(email_doador,email_interessado,nome_animal):
    #msg cria a mensgem que será enviada para o doador
    msg = Message(
        subject = f"interesse de adoção do pet {nome_animal}",
        #subject é o assunto do email

        recipients = [email_doador],
        #recipients é o destinatário do email (doador do pet)

        body = f'''Olá, um usuário se interessou pelo pet {nome_animal} que você cadastrou.
        
        caso tenha interesse em conversar com o usuário, responda ao e-mail
        do MatchPet, que encaminharemos a mensagem para o usuário interessado.
        
        Atenciosamente, Equipe MatchPet''',
        #aspas triplas para escrever o corpo do email em várias linhas

        reply_to = email_interessado
        #reply_to redireciona a resposta do email para o email do usuário interessado no pet
    )
    mail.send(msg)
