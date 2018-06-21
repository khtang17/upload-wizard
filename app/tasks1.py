import time
import sys
from rq import get_current_job
from app import create_app, db
from app.data.models.task import TaskModel
from app.data.models.user import UserModel
from app.data.models.catalog import CatalogModel
from flask import render_template
from app.email import send_email

app = create_app()
app.app_context().push()


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
        catalog = CatalogModel('test', 'mandatory', 'test', 804)
        catalog.save_to_db()
        user = UserModel.find_by_username("test")
        print("asdfasdf")
        print(user.email)
        for c in CatalogModel.find_by_history_id(804):
            print(c.field_name)
        send_email('You have granted access to system!',
                   sender='upload.vendor@gmail.com',
                   recipients=[user.email],
                   text_body=render_template('email/user_role_notify.txt', user=user),
                   html_body=render_template('email/user_role_notify.html', user=user), sync=True)
        # app.logger.error('Unhandled exception', exc_info="hi yu bn")
        # catalog = CatalogModel('test', 'mandatory', 'test', 804)
        # catalog.save_to_db()
        # user = UserModel.query.get(user_id)
        # user = UserModel.find_by_username("chinzo")
        # send_email('You have granted access to system!',
        #            sender='upload.vendor@gmail.com',
        #            recipients=[user.email],
        #            text_body=render_template('email/user_role_notify.txt', user=user),
        #            html_body=render_template('email/user_role_notify.html', user=user))
        # _set_task_progress(0)
        # data = []
        # i = 0
        # total_posts = 100
        # # for post in user.posts.order_by(Post.timestamp.asc()):
        # #     data.append({'body': post.body,
        # #                  'timestamp': post.timestamp.isoformat() + 'Z'})
        # #     time.sleep(5)
        # #     i += 1
        # #     _set_task_progress(100 * i // total_posts)
        # _set_task_progress(100)
        # # send email with data to user
    except:
        # ...
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())


def save_catalog_bulk_data(objects):
    try:
        app.logger.error('Unhandled exception', exc_info="hi yu bn")
        user = UserModel.query.get(1)
        from app.email import send_email
        send_email('You have granted access to system!',
                   sender='upload.vendor@gmail.com',
                   recipients=[user.email],
                   text_body=render_template('email/user_role_notify.txt', user=user),
                   html_body=render_template('email/user_role_notify.html', user=user))
    except:
        # ...
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())