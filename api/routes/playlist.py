from flask import Blueprint, jsonify, request
from api.models.music import Music
from api.services.token import read
from ytmusicapi import YTMusic

yt_music = YTMusic('headers_auth.json')
playlist = Blueprint('playlist', __name__)


@playlist.post('/createplaylist')
def create_playlist():
    token = request.headers.get('authorization')
    playlist_name = request.get_json()["name"]
    username = read(token)
    yt_music.create_playlist(
        str(len(playlist_name)) + ":" + playlist_name + username, username)
    return jsonify({'success': True}), 200


@playlist.post('/removeplaylist')
def remove_playlist():
    token = request.headers.get('authorization')
    playlistId = request.get_json()["id"]
    if yt_music.get_playlist(playlistId, 0)["description"] != read(token):
        return {"error": "Not your playlist"}, 400
    yt_music.delete_playlist(playlistId)
    return jsonify({'success': True}), 200


@playlist.post('/playlist/add')
def addmusic():
    token = request.headers.get('authorization')
    json = request.get_json()
    if yt_music.get_playlist(json["id"], 0)["description"] != read(token):
        return {"error": "Not your playlist"}, 400
    yt_music.add_playlist_items(json["id"], [json["videoid"]])
    return jsonify({'success': True}), 200


@playlist.post('/playlist/remove')
def remove_music_from_playlist():
    token = request.headers.get('authorization')
    json = request.get_json()
    if yt_music.get_playlist(json["id"], 0)["description"] != read(token):
        return {"error": "Not your playlist"}, 400
    yt_music.remove_playlist_items(
        json["id"], [{"videoId": json["videoid"], "setVideoId": json["setVideoId"]}])
    return jsonify({'success': True}), 200


@playlist.post('/playlist/check')
def check():
    token = request.headers.get('authorization')
    playlistId = request.get_json()["id"]
    if yt_music.get_playlist(playlistId, 0)["description"] != read(token):
        return "false", 200
    return "true", 200


@playlist.route('/getmyplaylist')
def get_my_playlist():
    token = request.headers.get('authorization')
    name = read(token)
    list = yt_music.get_library_playlists(10000)
    list1 = []
    for x in list:
        find = x["title"].find(":")
        temp = int(x["title"][0:find])
        if x["title"][temp + find + 1:] == name:
            x["title"] = x["title"][find + 1:temp + find + 1]
            list1.append(x)
    return jsonify(list1), 200


@playlist.post('/getotheruserplaylist')
def get_otheruser_playlist():
    json = request.get_json()
    list = yt_music.get_library_playlists(10000)
    list1 = []
    for x in list:
        find = x["title"].find(":")
        temp = int(x["title"][0:find])
        if x["title"][temp + find + 1:] == json["name"]:
            x["title"] = x["title"][find + 1:temp + find + 1]
            list1.append(x)
    return jsonify(list1), 200


@playlist.post('/getmusicfromplaylist')
def get_music_from_playlist():
    json = request.get_json()
    playlist = yt_music.get_playlist(json["id"])
    return jsonify(Music(playlist).dict), 200
