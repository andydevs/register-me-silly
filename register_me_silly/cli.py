"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from click import argument
from sqlalchemy.orm import load_only
from . import app
from .tasks import check_classes, check_class, test_tasks
from .model import ClassCheck


@app.cli.command()
def queue_check_classes():
    """
    Check all class records
    """
    check_classes.delay()


@app.cli.command()
@argument('id', type=int)
def queue_check_class(id):
    """
    Check class record with the given id
    """
    check_class.delay(id)


@app.cli.command()
def queue_test_tasks():
    """
    Test tasks system
    """
    result = test_tasks.delay()
    value = result.wait()
    print('It returned', value)
