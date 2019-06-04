"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from .celery import make_celery

# Create and configure app
app = Flask(__name__)
app.config.from_object('config.AppConfig')

# Declare components
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
celery = make_celery(app)

# Import parts
from . import views
from . import tasks
from . import cli
