from flask import Blueprint

application = Blueprint('api', __name__)

from app.api import job_log, errors, tokens