"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from random import randint
from datetime import datetime
from . import celery, db
from .model import ClassCheck
from .enrollment import has_enrollment_available
from .ifttt import trigger


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


@celery.task()
def test_tasks():
    """
    Celery task

    Test tasks system
    """
    print('Testing it out!')
    return randint(0, 0xffffffff)
