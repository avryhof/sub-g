import random

from subsonic_class import Subsonic


class GoogleResponse(object):
    source = "subsonic"

    session = None
    sub = None

    def __init__(self, session):
        self.session = session
        self.sub = Subsonic()

    def simple_response(self, text_response):
        resp = {
            "session": self.session,
            "prompt": {
                "override": False,
                "firstSimple": {
                    "speech": text_response,
                    "text": text_response
                }
            }
        }

        return resp

    def missing_parameter(self):
        return self.simple_response("Request problem: missing mandatory parameter.")

    def no_songs(self):
        return self.simple_response("No songs found.")

    def stream_song(self, song):
        if isinstance(song, str):
            song = self.sub.get_song(song)

        resp = {
            "session": self.session,
            "prompt": {
                "override": False,
                "content": {
                    "media": {
                        "mediaObjects": [
                            {
                                "name": song.get("title"),
                                "description": "{} by {}".format(song.get("title"), song.get("artist")),
                                "url": song.get("url"),
                                "image": {
                                    "large": {
                                        "alt": song.get("title"),
                                        "height": 0,
                                        "url": song.get("coverUrl"),
                                        "width": 0
                                    }
                                }
                            }
                        ],
                        "mediaType": "AUDIO",
                        "optionalMediaControls": [
                            "PAUSED",
                            "STOPPED"
                        ]
                    }
                },
                "firstSimple": {
                    "speech": "Playing %s" % song.get("title"),
                    "text": "Playing %s" % song.get("title")
                }
            }
        }

        return resp

    def stream_random(self, songs):
        if len(songs) == 0:
            retn = self.no_songs()
        else:
            song = random.choice(songs)
            retn = self.stream_song(song.get("id"))

        return retn

    def stream_songs(self, songs):
        if len(songs) == 0:
            retn = self.no_songs()
        else:
            song = songs[0]
            retn = self.stream_song(song.get("id"))

        return retn

    def random_song(self, artist=False):
        songs = self.sub.get_random_songs()

        return self.stream_songs(songs)

    def random_song_by_artist(self, artist):
        songs = self.sub.search2(artist, id3=True)

        return self.stream_random(songs)

    def song_by_artist(self, artist):
        songs = self.sub.search2(artist, id3=True)

        return self.stream_songs(songs)

    def song_by_genre(self, genre):
        songs = self.sub.get_songs_by_genre(genre)
        song = songs[0]

        self.stream_song(song.get("id"))

    def search(self, song, artist=False):
        if not song:
            retn = self.missing_parameter()
        else:
            songs = self.sub.search(song, artist)
            retn = self.stream_songs(songs)

        return retn

    def next_song(self):
        song = self.sub.find_next_song()

        if song is None:
            return self.no_songs()

        return self.stream_song(song.get("id"))
