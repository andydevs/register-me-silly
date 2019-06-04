"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from os import environ
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from sqlalchemy.orm import load_only
from celery.result import ResultSet
from .celery import make_celery
from .enrollment import has_enrollment_available
from .ifttt import trigger


# Create and configure app
app = Flask(__name__)
app.config['SECRET_KEY'] = environ['SECRET_KEY']
app.config['WTF_CSRF_SECRET_KEY'] = environ['WTF_CSRF_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CELERY_BROKER_URL'] = environ['REDIS_URL']
app.config['CELERY_RESULT_BACKEND'] = environ['REDIS_URL']
app.config['IFTTT_KEY'] = environ['IFTTT_KEY']


# Declare components
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
celery = make_celery(app)


# Import model
from . import views
from .model import ClassCheck


@celery.task()
def check_class(id):
    """
    Celery task

    Check class, update class record

    :param klass: class record
    """
    klass = ClassCheck.query.get(id)
    available = has_enrollment_available(klass.url)
    klass.last_checked = datetime.now()
    klass.available = available
    db.session.commit()
    if available:
        trigger('class_enroll_available',
            value1=klass.class_id,
            value2=klass.time_id)


@app.cli.command()
def queue_check_classes():
    """
    Check class record with the given id
    """
    classes = ClassCheck.query.options(load_only('id')).all()
    for klass in classes:
        check_class.delay(klass.id)
