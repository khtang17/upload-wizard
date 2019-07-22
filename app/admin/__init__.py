from flask import Blueprint

application = Blueprint('admin_views', __name__)

from app.admin import admin_routes
