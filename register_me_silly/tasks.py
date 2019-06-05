"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from random import randint
from datetime import datetime
from sqlalchemy.orm import load_only
from . import celery, db
from .model import ClassCheck
from .enrollment import has_enrollment_available
from .ifttt import trigger


@celery.task(ignore_result=True)
def check_classes():
    """
    Celery task

    Check all classes (queue tasks)
    """
    classes = ClassCheck.query.options(load_only('id')).all()
    for klass in classes:
        check_class.delay(klass.id)


@celery.task(ignore_result=True)
def check_class(id):
    """
    Celery task

    Check class, update class record

    :param klass: class record
    """
    print(f'[CHECK_CLASS({id})] Checking...')
    klass = ClassCheck.query.get(id)
    available = has_enrollment_available(klass.url)
    print(f'[CHECK_CLASS({id})] Available: {available}')
    klass.last_checked = datetime.now()
    klass.available = available
    db.session.commit()
    if available:
        print(f'[CHECK_CLASS({id})] Sending message...')
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
