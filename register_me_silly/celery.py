"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from celery import Celery

def make_celery(app):
    """
    Configure celery for app

    :param app: flask application instance
    """
    # Create and configure celery
    celery = Celery(app.import_name)
    celery.config_from_object('config.CeleryConfig')

    # Celery task using app context
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    # Return celery
    celery.Task = ContextTask
    return celery
