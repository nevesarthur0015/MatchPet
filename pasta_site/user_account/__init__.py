from flask import Blueprint

user_account_bp = Blueprint("user_account", __name__, template_folder= 'templates')

from . import routes
