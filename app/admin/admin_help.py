from sqlalchemy import extract
from flask import current_app
from flask_user import current_user
from app.constants import JOB_STATUS
from app.data.models.history import UploadHistoryModel
from datetime import datetime
from pdb import set_trace

def get_job_status_count():
   n = 0
   set_trace()
   this_month = datetime.today().month
   status_count = {}
   this_month_histories = UploadHistoryModel.get_this_month_upload(this_month)
   print(this_month_histories)
   for history in this_month_histories:
      if history.status_id in (3, 6, 9):
         n += 1
         status_count.update({'Failed': n})

   return n
