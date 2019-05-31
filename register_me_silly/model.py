"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from flask_sqlalchemy import SQLAlchemy
from codecs import decode
from csv import reader
from . import db


class ClassCheck(db.Model):
    """
    Class Check Model
    """
    __tablename__ = 'class_check'

    @classmethod
    def process_csv_file(cls, file):
        """
        Process csv file from post request

        :param file: file stream from post request
        """
        csv = reader(map(decode, file))
        classes = [
            ClassCheck(class_id=row[0], time_id=row[1], url=row[2])
            for row in csv
        ]
        db.session.bulk_save_objects(classes)
        db.session.commit()

    # Fields
    id = db.Column(db.Integer(), primary_key=True)
    class_id = db.Column(db.String())
    time_id = db.Column(db.String())
    url = db.Column(db.String())
    available = db.Column(db.Boolean(), default=False)
    last_checked = db.Column(db.Date())
