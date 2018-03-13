from app import app, db
from app.data.models.user import UserModel
from app.data.models.history import UploadHistoryModel
from app.data.models.format import FileFormatModel
from app.data.models.company import CompanyModel


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': UserModel, 'UploadHistory': UploadHistoryModel, 'FileFormat': FileFormatModel,
            'Company': CompanyModel}
