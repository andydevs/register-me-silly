"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from os import environ
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

# Create and configure app
app = Flask(__name__)
app.config['SECRET_KEY'] = environ['SECRET_KEY']
app.config['WTF_CSRF_SECRET_KEY'] = environ['WTF_CSRF_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Declare SQLALchemy
db = SQLAlchemy(app)


class ClassCheck(db.Model):
    """
    Class Check Model
    """
    id = db.Column(db.Integer(), primary_key=True)
    class_id = db.Column(db.String())
    time_id = db.Column(db.String())
    url = db.Column(db.String())
    available = db.Column(db.Boolean(), default=False)


class NewClassCheckForm(FlaskForm):
    """
    New Class Check Form
    """
    class_id = StringField('Class ID', validators=[DataRequired()])
    time_id = StringField('Time ID', validators=[DataRequired()])
    url = StringField('Check URL', validators=[DataRequired()])


# ClassCheck list view
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
            available=False)
        db.session.add(klass)
        db.session.commit()
    classes = ClassCheck.query.all()
    return render_template('index.html', form=form, classes=classes)


# ClassCheck delete
@app.route('/<class_id>/delete', methods=['POST'])
def delete_class(class_id):
    """
    Delete class view
    """
    if request.method == 'POST':
        klass = ClassCheck.query.filter_by(id=class_id).first_or_404()
        db.session.delete(klass)
        db.session.commit()
        return redirect('/')


# Check classes async task
    # Notify when done
    # Trigger every 15 minutes


# Create database model
db.create_all()
db.session.commit()
