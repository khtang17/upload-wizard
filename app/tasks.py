from celery import Celery
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# Be sure to add your SQS URL below!
#broker='sqs://AKIAJOX2FI6TLU6VKXSA:jGvsUp1FVBW+O46ZbRT5lHAP4fsL8OyBUix5SJaX@'
# application = Celery('tasks', broker='sqs://sqs.us-east-1.amazonaws.com/892261348956/flask-es')
application = Celery('tasks', broker='sqs://AKIAJOX2FI6TLU6VKXSA:jGvsUp1FVBW+O46ZbRT5lHAP4fsL8OyBUix5SJaX@')


# app = Flask(__name__)
# app.config
# db = SQLAlchemy(app)
# class ESConnection(AWSAuthConnection):
#     def __init__(self, region, **kwargs):
#         super(ESConnection, self).__init__(**kwargs)
#         self._set_auth_region_name(region)
#         self._set_auth_service_name("es")
#     def _required_auth_capability(self):
#         return ['hmac-v4']
#
#
# client = ESConnection(
#       region='us-east-1',
#       # host=' search-test-domain-ircp547akjoolsbp4ehu2a56u4.us-east-1.es.amazonaws.com',
#       host='uploadwizardeb-dev.us-west-1.elasticbeanstalk.com',
#       is_secure=False)

# app = create_app()
# app.app_context().push()


@application.task(name='tasks.get_location')
def get_location(catalog_dict):
        print("h1")
        print(catalog_dict)

        print("h2")
        # Get the location from the API
        # r = requests.get('http://freegeoip.net/json/' + address)
        # jstr = str(r.json()['latitude']) + ',' + str(r.json()['longitude'])
        # # Update the ElasticSearch index
        # resp = client.make_request(method='POST', path='/big_survey/quiz/' + user + '/_update',
        #                            data='{"doc":{"geo":"' + jstr + '"}}')
        return "return hi"