from app import create_app

# BEGIN CELERY
from celery import Celery


def make_celery(application):
    celery = Celery(application.import_name, broker=application.config['CELERY_BROKER_URL'])
    celery.conf.update(application.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with application.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
# DONE CELERY

application = create_app()

celery = make_celery(application)

#Celery Task
@celery.task(name='tasks.get_location')
def get_location(user):
        # Get the location from the API
        from app.data.models.catalog import CatalogModel
        catalog = CatalogModel('celery', 'celery', 'celery', 47)
        catalog.save_to_db()
        return
#End Task

@application.route('/test', methods=['GET', 'POST'])
def take_test():
    get_location.delay("")
    return "test"

if __name__ == '__main__':
    application.debug = True
    application.run()

# app.run(host='0.0.0.0', port=5001, debug=True)
