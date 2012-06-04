"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
from simplejson import loads

from flask import Flask, request
from sms import process

app = Flask(__name__)


if 'SECRET_KEY' in os.environ:
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
else:
    app.config['SECRET_KEY'] = 'this_should_be_configured'


@app.route('/', methods=['GET', 'POST'])
def issue():
    """Receive an incoming SMS message issue."""
    if request.method == 'POST':
        try:
            data = loads(request.data)
            text = data['inboundSMSMessageNotification']['inboundSMSMessage']
        except:
            return "Error."
        finally:
            process(text)
            return 'Success!'
    return "Not a POST request."


if __name__ == '__main__':
    app.run(debug=True)
