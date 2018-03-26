from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_user import UserManager, SQLAlchemyAdapter
from flask_moment import Moment
import flask_admin
from app.data.views.model_views import AdminModelView, UserView, RoleView, CompanyView, HistoryView
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
mail = Mail(app)
moment = Moment(app)
migrate = Migrate(app, db)
from app.data.models.user import UserModel
db_adapter = SQLAlchemyAdapter(db, UserModel)
user_manager = UserManager(db_adapter, app)
bootstrap = Bootstrap(app)


from app.data.models.company import CompanyModel
from app.data.models.user import RoleModel
from app.data.models.user import UserModel
from app.data.models.history import UploadHistoryModel


# Create admin
admin = flask_admin.Admin(
    app,
    'Vendor Upload v1.0: Admin Panel',
    base_template='master.html',
    template_mode='bootstrap3',
)

# Add model views
admin.add_view(HistoryView(UploadHistoryModel, db.session))
admin.add_view(CompanyView(CompanyModel, db.session))
admin.add_view(UserView(UserModel, db.session))


from app import routes, errors
from app.data import models
