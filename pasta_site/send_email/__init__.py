from flask import Blueprint

send_email_bp = Blueprint("send_email", __name__, template_folder= 'templates')

from . import routes