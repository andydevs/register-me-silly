"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from os import environ
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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
celery = make_celery(app)

# Import model
from .model import ClassCheck, NewClassCheckForm


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Class check list view
    """
    form = NewClassCheckForm()
    if form.validate_on_submit():
        klass = ClassCheck(
            class_id=form.class_id.data,
            time_id=form.time_id.data,
            url=form.url.data,
            available=False,
            last_checked=None)
        db.session.add(klass)
        db.session.commit()
    classes = ClassCheck.query.all()
    return render_template('index.html', form=form, classes=classes)


@app.route('/<id>/delete', methods=['POST'])
def delete_class(id):
    """
    Delete class view
    """
    if request.method == 'POST':
        klass = ClassCheck.query.filter_by(id=id).first_or_404()
        db.session.delete(klass)
        db.session.commit()
        return redirect('/')


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
