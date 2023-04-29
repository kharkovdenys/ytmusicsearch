class Music:
    def __init__(self, track):
        if 'album' in track and track['album']:
            self.album = track['album']['name']
        else:
            self.album = track['title']
        self.artists = " & ".join([artist["name"]
                                  for artist in track['artists']])
        if 'length' in track:
            self.duration = track['length']
        else:
            self.duration = track['duration']
        if 'thumbnail' in track:
            self.thumbnail = track['thumbnail'][0]['url']
        else:
            self.thumbnail = track['thumbnails'][0]['url']
        self.title = track['title']
        self.videoId = track['videoId']
        if 'setVideoId' in track:
            self.setVideoId = track['setVideoId']
        else:
            self.setVideoId = None

    def to_dict(self):
        return {
            'album': self.album,
            'artists': self.artists,
            'duration': self.duration,
            'thumbnail': self.thumbnail,
            'title': self.title,
            'videoId': self.videoId,
            'setVideoId': self.setVideoId
        }
