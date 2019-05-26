"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from flask import Flask, render_template

app = Flask(__name__)

# Declare SQLALchemy

# ClassCheck model
    # class id (string)
    # time id (string)
    # url (string)
    # available (bool)

# ClassCheck form
    # class id
    # time id
    # url

# ClassCheck list view
@app.route('/')
def index():
    """
    Class check list view
    """
    return render_template('index.html')

# Check classes async task
    # Notify when done
# Trigger every 15 minutes
