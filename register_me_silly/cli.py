"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from sqlalchemy.orm import load_only
from . import app
from .tasks import check_class
from .model import ClassCheck


@app.cli.command()
def queue_check_classes():
    """
    Check class record with the given id
    """
    classes = ClassCheck.query.options(load_only('id')).all()
    for klass in classes:
        check_class.delay(klass.id)
