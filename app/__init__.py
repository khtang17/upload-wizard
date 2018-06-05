__author__ = 'Chinzorig Dandarchuluun'
__copyright__ = "Copyright, UC Regents"


from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_user import UserManager, SQLAlchemyAdapter
from flask_moment import Moment
import flask_admin
from app.data.views.model_views import AdminModelView, UserView, RoleView, CompanyView, HistoryView, FieldView
from flask_mail import Mail
import flask_excel as excel

from flask_menu import Menu
# from flask_restful import Api

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


def create_app(config_class=Config):
    application = app = Flask(__name__)
    Menu(app=app)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    from app.data.models.user import UserModel

    db_adapter = SQLAlchemyAdapter(db, UserModel)
    user_manager = UserManager(db_adapter, app)
    # api.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    excel.init_excel(app)


    from app.data.models.company import CompanyModel
    from app.data.models.user import RoleModel
    from app.data.models.history import UploadHistoryModel
    from app.data.models.format import FileFormatModel
    from app.data.models.field_allowed_value import FieldAllowedValueModel
    from app.data.models.field_decimal import FieldDecimalModel
    from app.data.models.field import FieldModel

    # Create admin
    admin = flask_admin.Admin(
        app,
        'Vendor Upload v1.0: Admin Panel',
        base_template='master.html',
        template_mode='bootstrap3',
    )

    # Add model views
    admin.add_view(HistoryView(UploadHistoryModel, db.session, "History"))
    admin.add_view(CompanyView(CompanyModel, db.session, "Companies"))
    admin.add_view(UserView(UserModel, db.session, "Users"))
    admin.add_view(AdminModelView(FileFormatModel, db.session, "Column name"))
    admin.add_view(FieldView(FieldModel, db.session, "Excel file fields"))
    admin.add_view(AdminModelView(FieldDecimalModel, db.session, "Excel file Decimal column filter"))
    admin.add_view(AdminModelView(FieldAllowedValueModel, db.session, "Excel file column allowed values"))

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

    return app


from app.data import models
from app.main import routes