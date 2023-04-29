from flask import Flask, Response, request
from flask_cors import CORS
from api.routes.playlist_bp import playlist_bp
from api.routes.music_bp import music_bp

myapi = Flask(__name__)
CORS(myapi)


@myapi.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()


myapi.register_blueprint(music_bp)
myapi.register_blueprint(playlist_bp)
