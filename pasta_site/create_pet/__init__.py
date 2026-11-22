from flask import Blueprint

create_pet_bp = Blueprint("create_pet", __name__, template_folder= 'templates')

from . import routes