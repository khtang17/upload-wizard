from flask import Blueprint

application = Blueprint('main', __name__)


from application.main import routes