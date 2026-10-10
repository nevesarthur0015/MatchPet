from pasta_site import database,app

from pasta_site.models import Usuario,Foto

with app.app_context():
    database.create_all()