from flask import Blueprint, jsonify, request
from ytmusicapi import YTMusic
from api.models.music import Music
from api.models.playlist import Playlist

yt_music = YTMusic('browser.json')
music_bp = Blueprint('music_bp', __name__)


@music_bp.post('/get-similar-music-playlist')
def get_similar_music_playlist():
    """
    Get playlists of similar songs based on given music IDs.

    Returns:
        jsonify: Lists of similar songs with their details.
    """
    try:
        music_list = []
        request_data = request.get_json()
        for music in request_data:
            music_id = music['idVideo']
            playlist_tracks = yt_music.get_watch_playlist(music_id)['tracks']
            music_list.append([Music(track).to_dict()
                              for track in playlist_tracks])
        return jsonify(music_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@music_bp.post('/search')
def search_music():
    """
    Search for songs based on the given query.

    Returns:
        jsonify: A list of songs matching the query with their details.
    """
    try:
        request_data = request.get_json()
        query = request_data['query']
        search_list = yt_music.search(query, filter='songs')
        music_list = [[Music(track).to_dict()] for track in search_list]
        return jsonify(music_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@music_bp.post('/get-music-from-playlist')
def get_music_from_playlist():
    """
    Get the list of songs from the given playlist.

    Returns:
        jsonify: A list of songs in the playlist with their details.
    """
    try:
        request_data = request.get_json()
        playlist_id = request_data['id']
        playlist = Playlist(yt_music.get_playlist(playlist_id)).to_dict()
        return jsonify(playlist), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
