from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

RESPONSES_KEY = "responses"

app = Flask (__name__)
app.config['SECRET_KEY'] = "oh-so-secret" 
# config needs to be right after the file naming

debug = DebugToolbarExtension(app)