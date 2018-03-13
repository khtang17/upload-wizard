# import logging
# from logging.handlers import SMTPHandler
from flask import Flask, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from app.data.views.model_views import AdminModelView, UserView

import flask_admin
from flask_admin import helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# login = LoginManager(app)
# login.login_view = 'login'
# from app.data.models.user import UserModel
# db_adapter = SQLAlchemyAdapter(db, UserModel)
# user_manager = UserManager(db_adapter, app)
# user_manager.login_form = 'login'
bootstrap = Bootstrap(app)




from app.data.models.company import CompanyModel
from app.data.models.user import RoleModel
from app.data.models.user import UserModel

# Setup Flask-User and specify the User data-model

# if not CompanyModel.query.filter(CompanyModel.name == 'test').first():
#     company = CompanyModel(name='test',
#                            description='test',
#                            address='test',
#                            telephone_number='test',
#                            toll_free_number='test',
#                            fax_number='test',
#                            website='test',
#                            sales_email='test@mail.com')
#     db.session.add(company)
#     db.session.commit()
#
# # Create 'member@example.com' user with no roles
# if not UserModel.query.filter(UserModel.email == 'member@mail.com').first():
#     user = UserModel(
#         username='member',
#         email='member@mail.com',
#         company_id=1
#     )
#     user.set_password('member')
#     db.session.add(user)
#     db.session.commit()
#
# # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
# if not UserModel.query.filter(UserModel.email == 'admin@mail.com').first():
#     user = UserModel(
#         username='admin',
#         email='admin@mail.com',
#         company_id=1
#     )
#     user.set_password('admin')
#     user.roles.append(RoleModel(name='Admin'))
#     user.roles.append(RoleModel(name='Agent'))
#     db.session.add(user)
#     db.session.commit()


# # Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, UserModel, RoleModel)
security = Security(app, user_datastore)



# Create admin
admin = flask_admin.Admin(
    app,
    'Vendor Upload v1.0',
    base_template='my_master.html',
    template_mode='bootstrap3',
)
# Add model views
admin.add_view(AdminModelView(RoleModel, db.session))
admin.add_view(UserView(UserModel, db.session))


# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

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