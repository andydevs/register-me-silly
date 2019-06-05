"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from sqlalchemy.orm import load_only
from . import app
from .tasks import check_classes, test_tasks
from .model import ClassCheck


@app.cli.command()
def queue_check_classes():
    """
    Check class record with the given id
    """
    check_classes.delay()


@app.cli.command()
def queue_test_tasks():
    """
    Test tasks system
    """
    result = test_tasks.delay()
    value = result.wait()
    print('It returned', value)
