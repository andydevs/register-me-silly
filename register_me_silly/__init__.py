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

# Import parts
from . import views
from . import tasks
from . import cli
