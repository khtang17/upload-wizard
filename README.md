# Upload-wizard
Upload wizard web application

# Dependencies

* Python 3
* PostgreSQL
* SQLAlchemy

# Installation on Linux 

To clone repository 

```shell
git clone https://github.com/ChinzoD/upload-wizard.git
```
Create .env file into your project

```shell
cd upload-wizard
vim .env
```
Copy and paste below variables with your value into .env file

```shell
# Default email server is GMAIL. If you want to use other email, you need to 
# change MAIL_SERVER and MAIL_PORT in config.py
EMAIL = "your_email"
EMAIL_PASSWORD = "your_mail_password"

# AWS S3 configuration
S3_BUCKET = "your_s3_bucket"
S3_KEY = "your_access_key_id"
S3_SECRET = "your_secret_access_key "
S3_LOCATION = "your_s3_location" // http://folder.s3.amazonaws.com/sub_folder/

# You can use your local database or aws rds
SQLALCHEMY_DATABASE_URI_LOCAL = "postgresql+psycopg2://user:password:@localhost:6543/yout_database"
SQLALCHEMY_DATABASE_URI_AWS = "postgresql+psycopg2://user:password@your_db_instance_name:5432/db_name"

SECRET_KEY = ""
SECURITY_PASSWORD_SALT = ""
```
To install packages and run project 

```shell
pip install -r requirements.txt
python application.py
```

To export tar.gz archive file

```shell
python setup.py dir_name
```

## Authors

* **Chinzorig Dandarchuluun**

## License

Copyright © 2018
