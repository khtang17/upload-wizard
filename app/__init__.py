__author__ = 'Chinzorig Dandarchuluun'
__copyright__ = ""


from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_user import UserManager, SQLAlchemyAdapter
from flask_moment import Moment
import flask_admin
from app.data.views.model_views import AdminModelView, UserView, RoleView, \
    CompanyView, HistoryView, FieldView, MyHomeView, CatalogResult
from flask_mail import Mail
import flask_excel as excel
from flask_debugtoolbar import DebugToolbarExtension

from flask_menu import Menu
# # from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()
# api = Api()
mail = Mail()
moment = Moment()
bootstrap = Bootstrap()
# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
# mail = Mail(app)
# moment = Moment(app)
# migrate = Migrate(app, db)
# from app.data.models.user import UserModel
# db_adapter = SQLAlchemyAdapter(db, UserModel)
# user_manager = UserManager(db_adapter, app)
# bootstrap = Bootstrap(app)


def create_app(config_class=config):
    app = Flask(__name__)
    Menu(app=app)
    app.config.from_object(config['prod'])
    app.config.from_object(config_class)
    # toolbar = DebugToolbarExtension(app)
    # toolbar.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    from app.data.models.user import UserModel

    db_adapter = SQLAlchemyAdapter(db, UserModel)
    user_manager = UserManager(db_adapter, app)
    user_manager.resend_confirm_email_view_function
    # api.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    excel.init_excel(app)

    from app.data.models.company import CompanyModel
    from app.data.models.user import RoleModel
    from app.data.models.status import StatusModel
    from app.data.models.history import UploadHistoryModel
    from app.data.models.format import FileFormatModel
    from app.data.models.field_allowed_value import FieldAllowedValueModel
    from app.data.models.field_decimal import FieldDecimalModel
    from app.data.models.field import FieldModel
    from app.data.models.job_log import JobLogModel
    from app.data.models.catalog_info import CatalogResultInfo

    # Create admin
    admin = flask_admin.Admin(
        app,
        'Upload Wizard v1.0: Admin Panel',
        index_view=MyHomeView(),
        base_template='master.html',
        template_mode='bootstrap3',
    )

    # Add model views
    admin.add_view(HistoryView(UploadHistoryModel, db.session, "History"))
    admin.add_view(CompanyView(CompanyModel, db.session, "Companies"))
    admin.add_view(UserView(UserModel, db.session, "Users"))
    admin.add_view(CatalogResult(CatalogResultInfo, db.session, "Catalog Results"))

    if app.config['ZINC_MODE']:
        admin.add_view(AdminModelView(FileFormatModel, db.session, "Column name"))
    else:
        # admin.add_view(ResultView(name='result', endpoint='result'))
        admin.add_view(FieldView(FieldModel, db.session, "File fields"))
        admin.add_view(AdminModelView(FieldDecimalModel, db.session, "File Decimal column filter"))
        admin.add_view(AdminModelView(FieldAllowedValueModel, db.session, "File column allowed values"))

    # from flask_jwt import JWT
    # from security import authenticate, identity
    # from app.data.resources.history import HistoryList
    # jwt = JWT(app, authenticate, identity)  # /auth
    # api.add_resource(HistoryList, '/histories1')

    from app.errors import application as errors_bp
    app.register_blueprint(errors_bp)

    from app.api import application as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.main import application as main_bp
    app.register_blueprint(main_bp)

    from app.admin import admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app


from app.data import models
