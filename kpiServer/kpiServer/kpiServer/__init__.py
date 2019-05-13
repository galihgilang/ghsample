# http://flask.pocoo.org/docs/1.0/patterns/packages/
from flask import Flask
app = Flask(__name__)

import kpiServer.views