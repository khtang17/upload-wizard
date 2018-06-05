from flask import Blueprint

application = Blueprint('errors', __name__)

from application.errors import handlers
