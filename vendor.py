from app import app, db
from app.data.models import User, UploadHistory, FileFormat, Company

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'UploadHistory': UploadHistory, 'FileFormat': FileFormat, 'Company': Company}