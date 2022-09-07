from flask import Flask
from flask_cors import CORS
from api.routes.playlist import playlist
from api.routes.search import search
from api.routes.mix import mix

myapi = Flask(__name__)
CORS(myapi)

myapi.register_blueprint(playlist)
myapi.register_blueprint(search)
myapi.register_blueprint(mix)
