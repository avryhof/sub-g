import pprint
import random
import string

import requests
from django.conf import settings

from .exceptions import InvalidCriteria
from subsonic_tools import md5


class Subsonic(object):
    app_name = "Subsonic Class"
    api_version = "1.16.1"
    debug = False

    endpoint = None
    username = None
    password = None

    salt = None
    encoded_password = None

    def __init__(self, **kwargs):
        self.debug = kwargs.get("debug", False)

        self.endpoint = kwargs.get("url", settings.SUBSONIC_URL)
        self.username = kwargs.get("user", settings.SUBSONIC_USER)
        self.password = kwargs.get("password", settings.SUBSONIC_PASSWORD)

        salt_length = random.randint(6, 12)
        self.salt = "".join(
            random.choice(string.ascii_letters + "1234567890_")
            for i in range(salt_length)
        )

        salted_password = self.password + self.salt
        self.encoded_password = md5(salted_password)

    def _api_call(self, resource, data={}):
        api_data = dict(
            u=self.username,
            t=self.encoded_password,
            s=self.salt,
            v=self.api_version,
            c=self.app_name,
            f="json",
        )

        if isinstance(data, dict):
            for k, v in data.items():
                api_data[k] = v

        url = "{}/rest/{}.view".format(self.endpoint, resource)

        if self.debug:
            print(url)
            pprint.pprint(api_data)

        resp = requests.get(url, params=api_data)

        if self.debug:
            print(resp)

        return resp.json()

    def download(self, song_id=False):
        if not song_id:
            song = self.now_playing()
            song_id = song.get("id")
        return self._api_call("download", dict(id=song_id))

    def find_next_song(self, song_id):
        current_song = self.get_song(song_id)
        if not current_song or not "parent" in current_song:
            return None

        directory = self.music_directory(current_song.get("parent"))
        if not directory or not "child" in directory:
            return None

        is_current_song = False
        for child in directory.get("child"):
            if child.get("isDir"):
                continue

            if is_current_song:
                child["url"] = self.stream(child.get("id"))
                child["coverUrl"] = self.get_cover_art(child.get("id"))
                return child

            if child.get("id") == song_id:
                is_current_song = True

        return None

    def get_album(self, album_id):
        resp = self._api_call("getAlbum", dict(id=album_id))
        album = resp.get("subsonic-response", {}).get("album")

        return album

    def get_cover_art(self, song_id):
        return self._api_call("getCoverArt", dict(id=song_id))

    def get_genres(self):
        resp = self._api_call("getGenres")
        genres = resp.pget("subsonic-response", {}).get("genres", {}).get("genre")

        return genres

    def get_random_songs(self):
        search_result = self._api_call("getRandomSongs")
        songs = search_result.get("subsonic-response", {}).get("randomSongs", {}).get("song", [])

        return songs

    def get_song(self, song_id):
        resp = self._api_call("getSong", dict(id=song_id))
        song = resp.get("subsonic-response", {}).get("song")

        return song

    def get_songs_by_genre(self, genre):
        return self._api_call("getSongsByGenre")

    def music_directory(self, parent_id):
        return self._api_call("getMusicDirectory", dict(id=parent_id))

    def now_playing(self):
        return self._api_call("getNowPlaying")

    def ping(self):
        return self._api_call("ping")

    def search(self, song, artist=False, count=1):
        songs = self.search2(song, id3=True, result_type="song")

        if artist:
            songs_by_artist = []
            for song in songs:
                song_artist = song.get("artist")
                if song_artist and artist.lower() in song.get("artist").lower():
                    songs_by_artist.append(song)
            songs = songs_by_artist

        if count:
            songs = songs[0:count]

        return songs

    def search2(self, query, **kwargs):
        # Default to searching everything
        resource = "search2"
        result_key = "searchResult2"
        result_type = "song"

        data = dict(query=query)

        if "id3" in kwargs:
            # If id3=True is passed as a keyword argument, we search in id3 tags rather than all inferred data
            if kwargs.pop("id3", False):
                resource = "search3"
                result_key = "searchResult3"

        if "result_type" in kwargs:
            # We can limit result type to: album, artist, or song
            result_type = kwargs.pop("result_type")

            if result_type not in ["album", "artist", "song"]:
                raise InvalidCriteria("result_type must be album, artist, or song")

        if kwargs:
            data.update(kwargs)

        result = self._api_call(resource, data)
        search_results = result.get("subsonic-response", {}).get(result_key)

        if isinstance(result_type, str):
            search_results = search_results.get(result_type)

        return search_results

    def stream(self, song_id):
        return self._api_call("stream", dict(id=song_id))
