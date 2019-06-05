"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from os import environ
from celery.schedules import crontab

class AppConfig:
    """
    Application config
    """
    SECRET_KEY = environ['SECRET_KEY']
    WTF_CSRF_SECRET_KEY = environ['WTF_CSRF_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    IFTTT_KEY = environ['IFTTT_KEY']


class CeleryConfig:
    """
    Celery task runner config
    """
    BROKER_URL = environ['REDIS_URL']
    CELERY_RESULT_BACKEND = environ['REDIS_URL']
    CELERY_TASK_SERIALIZER = 'json'
    CELERYBEAT_SCHEDULE = {
        'schedule-check-classes' : {
            'task': 'tasks.check_classes',
            'schedule': crontab(minute='*/15')
        }
    }
