from flask import Flask
from flask_restful import Api
from flask__pymongo import PyMongo

app = Flask(__name__)
api = Api(app)

# Setup MongoDB
mongodb_client = PyMongo(app)
db = mongodb_client.db

# For CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

from api import routes