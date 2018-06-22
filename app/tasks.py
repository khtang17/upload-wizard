from app import create_app
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# Be sure to add your SQS URL below!
#broker='sqs://AKIAJOX2FI6TLU6VKXSA:jGvsUp1FVBW+O46ZbRT5lHAP4fsL8OyBUix5SJaX@'
# application = Celery('tasks', broker='sqs://sqs.us-east-1.amazonaws.com/892261348956/flask-es')
# application = Celery('tasks', broker='sqs://AKIAJOX2FI6TLU6VKXSA:jGvsUp1FVBW+O46ZbRT5lHAP4fsL8OyBUix5SJaX@')

app = create_app()
app.app_context().push()

#Celery Task
@app.celery.task(name='tasks.get_location', queue="flask-es")
def get_location(user):
        # Get the location from the API
        from app.data.models.catalog import CatalogModel
        catalog = CatalogModel('celery', 'celery', 'celery', 47)
        catalog.save_to_db()
        return
#End Task

# @application.task(name='tasks.get_location')
# def get_location(catalog_dict):
#         print("h1")
#         print(catalog_dict)
#
#         print("h2")
#         # Get the location from the API
#         # r = requests.get('http://freegeoip.net/json/' + address)
#         # jstr = str(r.json()['latitude']) + ',' + str(r.json()['longitude'])
#         # # Update the ElasticSearch index
#         # resp = client.make_request(method='POST', path='/big_survey/quiz/' + user + '/_update',
#         #                            data='{"doc":{"geo":"' + jstr + '"}}')
#         return "return hi"