from flask import Blueprint, jsonify, request
from ytmusicapi import YTMusic

from api.models.music import Music

yt_music = YTMusic('headers_auth.json')
search = Blueprint('search', __name__)


@search.post('/search')
def search_music():
    query = request.get_json()["query"]
    response = yt_music.search(query, filter='songs')
    for element in response:
        element = Music(element).dict
    return jsonify(response), 200
