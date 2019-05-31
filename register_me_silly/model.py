"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from flask_sqlalchemy import SQLAlchemy
from . import db


class ClassCheck(db.Model):
    """
    Class Check Model
    """
    __tablename__ = 'class_check'

    # Fields
    id = db.Column(db.Integer(), primary_key=True)
    class_id = db.Column(db.String())
    time_id = db.Column(db.String())
    url = db.Column(db.String())
    available = db.Column(db.Boolean(), default=False)
    last_checked = db.Column(db.Date())
