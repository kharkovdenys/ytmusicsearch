import jwt
from flask import Flask, jsonify, request
from ytmusicapi import YTMusic
from flask_cors import CORS

myapi = Flask(__name__)
yt_music = YTMusic('headers_auth.json')
CORS(myapi)


def read(token):
    return jwt.decode(token, "_webmusic-chaha_", algorithms=['HS256'], audience="chaha")[
        "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"]


@myapi.post('/search')
def search_music():
    if request.is_json:
        json = request.get_json()
        response = yt_music.search(json["query"], filter='songs')
        for element in response:
            element["thumbnail"] = element["thumbnails"]
            element["length"] = element["duration"]
            del element["category"], element["duration_seconds"], element["feedbackTokens"], element["thumbnails"]
            del element["isExplicit"], element["year"], element["resultType"], element["duration"]
        return jsonify(response), 201
    return {"error": "Request must be JSON"}, 415


@myapi.post('/getmusicmix')
def get_music_mix():
    if request.is_json:
        json = request.get_json()
        list = []
        for x in json:
            response = yt_music.get_watch_playlist(x["idVideo"])
            del response["lyrics"], response["playlistId"]
            list.append(response)
        return jsonify(list), 201
    return {"error": "Request must be JSON"}, 415


@myapi.post('/createplaylist')
def create_playlist():
    if request.is_json:
        token = request.headers.get('authorization')
        json = request.get_json()
        name = read(token)
        yt_music.create_playlist(str(len(json["name"])) + ":" + json["name"] + name, name)
        return jsonify({'success': True}), 201
    return {"error": "Request must be JSON"}, 415


@myapi.post('/removeplaylist')
def remove_playlist():
    if request.is_json:
        token = request.headers.get('authorization')
        json = request.get_json()
        if yt_music.get_playlist(json["id"], 0)["description"] != read(token):
            return {"error": "Not your playlist"}, 415
        yt_music.delete_playlist(json["id"])
        return jsonify({'success': True}), 201
    return {"error": "Request must be JSON"}, 415


@myapi.post('/playlist/add')
def addmusic():
    if request.is_json:
        token = request.headers.get('authorization')
        json = request.get_json()
        if yt_music.get_playlist(json["id"], 0)["description"] != read(token):
            return {"error": "Not your playlist"}, 415
        yt_music.add_playlist_items(json["id"], [json["videoid"]])
        return jsonify({'success': True}), 201
    return {"error": "Request must be JSON"}, 415


@myapi.post('/playlist/remove')
def remove_music_from_playlist():
    if request.is_json:
        token = request.headers.get('authorization')
        json = request.get_json()
        if yt_music.get_playlist(json["id"], 0)["description"] != read(token):
            return {"error": "Not your playlist"}, 415
        yt_music.remove_playlist_items(json["id"], [json["videoid"]])
        return jsonify({'success': True}), 201
    return {"error": "Request must be JSON"}, 415


@myapi.get('/getmyplaylist')
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
    return jsonify(list1), 201


@myapi.post('/getotheruserplaylist')
def get_otheruser_playlist():
    if request.is_json:
        json = request.get_json()
        list = yt_music.get_library_playlists(10000)
        list1 = []
        for x in list:
            find = x["title"].find(":")
            temp = int(x["title"][0:find])
            if x["title"][temp + find + 1:] == json["name"]:
                x["title"] = x["title"][find + 1:temp + find + 1]
                list1.append(x)
        return jsonify(list1), 201
    return {"error": "Request must be JSON"}, 415


@myapi.post('/getmusicfromplaylist')
def get_music_from_playlist():
    if request.is_json:
        json = request.get_json()
        playlist = yt_music.get_playlist(json["id"])
        for element in playlist["tracks"]:
            element["thumbnail"] = element["thumbnails"]
            element["length"] = element["duration"]
            del element["thumbnails"], element["duration"]
        return jsonify(playlist), 201
    return {"error": "Request must be JSON"}, 415
