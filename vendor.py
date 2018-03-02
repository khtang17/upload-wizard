from app import app, db
from app.data.models.user import User
from app.data.models.history import UploadHistory
from app.data.models.format import FileFormat
from app.data.models.company import  Company

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'UploadHistory': UploadHistory, 'FileFormat': FileFormat, 'Company': Company}