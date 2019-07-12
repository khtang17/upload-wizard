from flask import Blueprint

application = Blueprint('main', __name__)


from app.main import routes, users_routes, catalog_jobs_routes