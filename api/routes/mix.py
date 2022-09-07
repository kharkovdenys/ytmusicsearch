from flask import Blueprint, jsonify, request
from ytmusicapi import YTMusic
from api.models.music import Music

yt_music = YTMusic('headers_auth.json')
mix = Blueprint('mix', __name__)


@mix.post('/getmusicmix')
def get_music_mix():
    json = request.get_json()
    list = []
    for x in json:
        list.append(Music(yt_music.get_watch_playlist(x["idVideo"])).dict)
    return jsonify(list), 200
