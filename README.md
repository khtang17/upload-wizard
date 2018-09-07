# Upload-wizard
Upload wizard web application

Python 3

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
MAIL_PASSWORD = "your_mail_password"
S3_BUCKET = "your_s3_bucket"
S3_KEY = "your_access_key_id"
S3_SECRET = "your_secret_access_key "
S3_LOCATION = "your_s3_location" // http://folder.s3.amazonaws.com/sub_folder/

// you can use your local database or aws rds
SQLALCHEMY_DATABASE_URI_LOCAL = "postgresql+psycopg2://your_db_password:@localhost:6543/yout_database"
SQLALCHEMY_DATABASE_URI_AWS = "postgresql+psycopg2://user:password@your_db_instance_name:5432/db_name"

SECRET_KEY = ""
SECURITY_PASSWORD_SALT = ""
```
To install packages and run project 

```shell
pip install -r requirements.txt
python application.py
```

## Authors

* **Chinzorig Dandarchuluun**

## License

Copyright © 2018
