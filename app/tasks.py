import time
from rq import get_current_job
from app import db
from app.data.models.task import TaskModel
from app.data.models.user import UserModel


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = TaskModel.query.get(job.get_id())
        task.user.add_notification('task_progress', {'task_id': job.get_id(),
                                                     'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()


def example(seconds):
    job = get_current_job()
    print('Starting task')
    for i in range(seconds):
        job.meta['progress'] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task completed')


def export_posts(user_id):
    try:
        user = UserModel.query.get(user_id)
        _set_task_progress(0)
        data = []
        i = 0
        total_posts = 100
        # for post in user.posts.order_by(Post.timestamp.asc()):
        #     data.append({'body': post.body,
        #                  'timestamp': post.timestamp.isoformat() + 'Z'})
        #     time.sleep(5)
        #     i += 1
        #     _set_task_progress(100 * i // total_posts)
        _set_task_progress(100)
        # send email with data to user
    except:
        # ...
        _set_task_progress(100)
        # app.logger.error('Unhandled exception', exc_info=sys.exc_info())


def save_catalog_bulk_data(objects):
    try:
        print("1")
        print(objects)
        _set_task_progress(0)
        i = 0
        total_objects = len(objects)
        for o in objects:
            db.session.add(o)
            i += 1
            print(i)
            _set_task_progress(100 * i // total_objects)
        db.session.commit()
    except:
        # ...
        _set_task_progress(100)
