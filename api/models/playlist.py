from api.models.music import Music


class Playlist:
    def __init__(self, playlist):
        find = playlist["title"].find(":")
        self.title = playlist["title"][find+1:find +
                                       int(playlist["title"][0:find])+1]
        if 'count' in playlist:
            self.count = playlist['count']
        else:
            self.count = playlist['trackCount']
        if 'playlistId' in playlist:
            self.playlistId = playlist['playlistId']
        else:
            self.playlistId = playlist['id']
        self.thumbnail = playlist['thumbnails'][0]['url']
        if 'tracks' in playlist:
            self.tracks = [Music(track).to_dict()
                           for track in playlist['tracks']]
        else:
            self.tracks = []

    def to_dict(self):
        return {
            'title': self.title,
            'count': self.count,
            'playlistId': self.playlistId,
            'thumbnail': self.thumbnail,
            'tracks': self.tracks
        }
