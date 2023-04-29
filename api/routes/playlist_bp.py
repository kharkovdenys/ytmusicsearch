from flask import Blueprint, jsonify, request
from api.models.playlist import Playlist
from api.services.token import read
from ytmusicapi import YTMusic

yt_music = YTMusic('browser.json')
playlist_bp = Blueprint('playlist', __name__)


@playlist_bp.post('/create_playlist')
def create_playlist():
    """
    Create a new playlist with the given name for the authenticated user.

    Returns:
        jsonify: A success message.
    """
    try:
        token = request.headers.get('authorization')
        request_data = request.get_json()
        playlist_name = request_data["name"]
        username = read(token)
        playlist_title = f"{len(playlist_name)}:{playlist_name}{username}"
        yt_music.create_playlist(playlist_title, username)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@playlist_bp.post('/remove_playlist')
def remove_playlist():
    """
    Remove the playlist with the given ID for the authenticated user.

    Returns:
        jsonify: A success message.
    """
    try:
        token = request.headers.get('authorization')
        request_data = request.get_json()
        playlist_id = request_data["id"]
        playlist_desc = yt_music.get_playlist(playlist_id, 0)["description"]
        if playlist_desc != read(token):
            return {"error": "Not your playlist"}, 400
        yt_music.delete_playlist(playlist_id)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@playlist_bp.post('/playlist/add')
def add_music():
    """
    Add a new music to the playlist with the given ID for the authenticated user.

    Returns:
        jsonify: A success message.
    """
    try:
        token = request.headers.get('authorization')
        request_data = request.get_json()
        playlist_id = request_data["id"]
        music_id = request_data["videoId"]
        if yt_music.get_playlist(playlist_id, 0)["description"] != read(token):
            return {"error": "Not your playlist"}, 400
        yt_music.add_playlist_items(playlist_id, [music_id])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@playlist_bp.post('/playlist/remove')
def remove_music_from_playlist():
    """
    Remove a music from the playlist with the given ID for the authenticated user.

    Returns:
        jsonify: A success message.
    """
    try:
        token = request.headers.get('authorization')
        request_data = request.get_json()
        playlist_id = request_data["id"]
        music_id = request_data["videoId"]
        set_music_id = request_data["setVideoId"]
        if yt_music.get_playlist(playlist_id, 0)["description"] != read(token):
            return {"error": "Not your playlist"}, 400
        yt_music.remove_playlist_items(
            playlist_id, [{"videoId": music_id, "setVideoId": set_music_id}])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@playlist_bp.post('/playlist/check')
def check():
    """
    Check if the authenticated user has access to the playlist with the given ID.

    Returns:
        jsonify: A success message.
    """
    try:
        token = request.headers.get('authorization')
        playlist_id = request.get_json()["id"]
        if yt_music.get_playlist(playlist_id, 0)["description"] != read(token):
            return jsonify({'result': False}), 200
        return jsonify({'result': True}), 200
    except:
        return jsonify({'result': False}), 200


@playlist_bp.post('/user-playlists')
def get_user_playlists():
    """
    Get a list of playlists for the authenticated user.

    Returns:
        jsonify: User playlists.
    """
    try:
        request_data = request.get_json()
        if 'name' in request_data:
            username = request_data['name']
        else:
            token = request.headers.get('authorization')
            username = read(token)
        playlists = yt_music.get_library_playlists(10000)
        user_playlists = []
        for playlist in playlists:
            find = playlist["title"].find(":")
            if find > 0 and playlist["title"][int(playlist["title"][0:find]) + find + 1:] == username:
                user_playlists.append(Playlist(playlist).to_dict())
        return jsonify(user_playlists), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
