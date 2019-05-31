"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField
from wtforms.validators import DataRequired

class NewClassCheckForm(FlaskForm):
    """
    New Class Check Form
    """
    class_id = StringField('Class ID', validators=[DataRequired()])
    time_id = StringField('Time ID', validators=[DataRequired()])
    url = StringField('Check URL', validators=[DataRequired()])


class UploadCSVForm(FlaskForm):
    """
    Form to upload CSV file with class check data
    """
    csv = FileField('CSV File', validators=[
        FileRequired(),
        FileAllowed(['csv'])
    ])
