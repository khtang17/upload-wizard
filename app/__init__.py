from flask import Flask, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_user import UserManager, SQLAlchemyAdapter

import flask_admin
from app.data.views.model_views import AdminModelView, UserView, RoleView, CompanyView



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app.data.models.user import UserModel
db_adapter = SQLAlchemyAdapter(db, UserModel)
user_manager = UserManager(db_adapter, app)
bootstrap = Bootstrap(app)


from app.data.models.company import CompanyModel
from app.data.models.user import RoleModel
from app.data.models.user import UserModel


# Create admin
admin = flask_admin.Admin(
    app,
    'Vendor Upload v1.0',
    base_template='master.html',
    template_mode='bootstrap3',
)

# Add model views
admin.add_view(RoleView(RoleModel, db.session))
admin.add_view(UserView(UserModel, db.session))
admin.add_view(CompanyView(CompanyModel, db.session))
# admin.add_view(UploadView(name='File Upload', endpoint='upload'))


# define a context processor for merging flask-admin's template context into the
# flask-security views.
# @security.context_processor
# def security_context_processor():
#     return dict(
#         admin_base_template=admin.base_template,
#         admin_view=admin.index_view,
#         h=admin_helpers,
#         get_url=url_for
#     )


from app import routes, errors
from app.data import models


# if not app.debug:
#     if app.config['MAIL_SERVER']:
#         auth = None
#         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
#             auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
#         secure = None
#         if app.config['MAIL_USE_TLS']:
#             secure = ()
#         mail_handler = SMTPHandler(
#             mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
#             fromaddr='no-reply@' + app.config['MAIL_SERVER'],
#             toaddrs=app.config['ADMINS'], subject='Microblog Failure',
#             credentials=auth, secure=secure)
#         mail_handler.setLevel(logging.ERROR)
#         app.logger.addHandler(mail_handler)