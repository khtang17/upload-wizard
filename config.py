import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    SECURITY_PASSWORD_SALT = 'Nuut9davs'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              # 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://uploadwrite:@localhost:6543/uploaddb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_MAX_OVERFLOW = 5
    SQLALCHEMY_POOL_TIMEOUT = 10
    LISTS_PER_PAGE = 20
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024
    UPLOAD_FOLDER = '/nfs/ex5/vendoruploads/'
    LOGO_UPLOAD_FOLDER = '/nfs/ex5/vendoruploads/vendorlogos/'
    # LOGO_UPLOAD_FOLDER = 'app/static/vendorlogos/'
    LOGO_UPLOAD_FOLDER_URL = 'http://files.docking.org/vendorlogos/'
    # LOGO_UPLOAD_FOLDER_URL = 'static/vendorlogos/'

    # REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    AWS_REGION = 'us-east-1'
    NEW_SIGNUP_TOPIC = 'your_sns_topic_name'
    STARTUP_SIGNUP_TABLE = 'your_ddb_table_name'
    THEME = 'default'
    FLASK_DEBUG = 'true'

    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False

    ZINC_MODE = False
    FILE_VALIDATION_LIMIT = 500000

    # Flask-Mail SMTP account settings
    MAIL_USERNAME = 'upload.vendor@gmail.com'
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = 'upload.vendor@gmail.com'

    # Flask-User settings
    USER_APP_NAME = "Upload Wizard Team"  # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True  # Enable email authentication
    USER_ENABLE_USERNAME = True  # Register and Login with username
    USER_LOGIN_TEMPLATE = 'flask_user/login_or_register.html'
    USER_REGISTER_TEMPLATE = 'flask_user/login_or_register.html'
    USER_LOGOUT_URL = '/user/logout'
    USER_LOGIN_URL = '/user/login'
    USER_ENABLE_FORGOT_PASSWORD = True
    USER_AFTER_LOGIN_ENDPOINT = 'main.index'
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "upload.vendor@gmail.com"

    CSRF_ENABLED = True

    SCRIPT_SOURCE = ''

    S3_BUCKET = ""
    S3_KEY = ""
    S3_SECRET = ""
    S3_LOCATION = ""