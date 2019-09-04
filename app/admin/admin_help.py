from sqlalchemy import extract
from flask import current_app
from flask_user import current_user
from app.constants import JOB_STATUS
from app.data.models.history import UploadHistoryModel
from datetime import datetime
from pdb import set_trace

def get_job_status_count():
   status_count = {}
   this_month_histories = UploadHistoryModel.get_this_month_upload()
   job_count = 0
   attention = failed = finished = running = 0
   for history in this_month_histories:
      job_count +=1
      if history.status_id in (3, 6, 9):
         failed += 1
         status_count.update({'Failed': failed})
      elif history.status_id == 11:
         finished += 1
         status_count.update({'Finished' : finished})
      elif history.status_id == 15:
         attention += 1
         status_count.update({'Attention' : attention})
      else:
         running += 1
         print(history)
         status_count.update({'Running' : running})

   return status_count, job_count
