from flask import Flask
from flask.ext.restful import Api
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
api = Api(app)

app.config['MONGODB_SETTINGS'] = {'DB': 'stars'}
db = MongoEngine(app)

from . import views
