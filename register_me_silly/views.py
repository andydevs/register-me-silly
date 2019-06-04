"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from flask import render_template, request, redirect, flash
from . import app, db
from .model import ClassCheck
from .forms import NewClassCheckForm, UploadCSVForm


@app.route('/', methods=['GET'])
def index():
    """
    Class check list view
    """
    new_class_check_form = NewClassCheckForm()
    upload_csv_form = UploadCSVForm()
    classes = ClassCheck.query.all()
    return render_template('index.html',
        new_class_check_form=new_class_check_form,
        upload_csv_form=upload_csv_form,
        classes=classes)


@app.route('/new-class-check', methods=['POST'])
def new_class_check():
    """
    New Class Check record
    """
    new_class_check_form = NewClassCheckForm()
    if new_class_check_form.validate_on_submit():
        klass = ClassCheck(
            class_id=new_class_check_form.class_id.data,
            time_id=new_class_check_form.time_id.data,
            url=new_class_check_form.url.data,
            available=False,
            last_checked=None)
        db.session.add(klass)
        db.session.commit()
        flash('New class check added!', 'success')
    return redirect('/')


@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    """
    Upload csv file
    """
    upload_csv_form = UploadCSVForm()
    if upload_csv_form.validate_on_submit():
        file = upload_csv_form.csv.data
        ClassCheck.process_csv_file(file)
        flash('CSV file uploaded!', 'success')
    return redirect('/')


@app.route('/<id>/delete', methods=['POST'])
def delete_class(id):
    """
    Delete class view
    """
    if request.method == 'POST':
        klass = ClassCheck.query.filter_by(id=id).first_or_404()
        db.session.delete(klass)
        db.session.commit()
        flash('Class check deleted!', 'success')
    return redirect('/')
