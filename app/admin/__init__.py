from flask import Blueprint
#
# application = Blueprint('admin_views', __name__)
#


admin_blueprint = Blueprint('admin_views', __name__, url_prefix='/admin',
template_folder='templates/admin', static_folder='../static')

from app.admin import admin_routes