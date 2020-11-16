from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from google_responses import GoogleResponse
from oauthprovider.api_auth import AnonymousAuthentication
from oauthprovider.constants import NO_CACHE_HEADERS
from oauthprovider.permissions import AnonymousPermission


@api_view(["POST"])
@authentication_classes((AnonymousAuthentication,))
@permission_classes((AnonymousPermission,))
def intent_responder(request):
    resp = {}

    # log_message(type(request.data))
    # log_message(request.data)

    intent = request.data.get("intent", {})

    query = intent.get("query")
    params = intent.get("params")
    session = request.data.get("session")

    # print(query)
    # pprint.pprint(params)

    action = "Play"
    artist = False
    song = False
    genre = False
    song_type = False

    if "action" in params:
        action = params.get("action", {}).get("resolved")

    if "artist" in params:
        artist = params.get("artist", {}).get("resolved")

    if "song" in params:
        song = params.get("song", {}).get("resolved")

    if "song_type" in params:
        song_type = params.get("song_type", {}).get("resolved")

    if "genre" in params:
        genre = params.get("genre", {}).get("resolved")

    google_resp = GoogleResponse(session)
    if action == "Shuffle":
        if artist:
            resp = google_resp.random_song_by_artist(artist)
        elif genre:
            resp = google_resp.song_by_genre(genre)
        else:
            resp = google_resp.random_song()

    elif action == "Play":
        if song and not artist and "by" in song.lower():
            parts = song.lower().split("by")
            artist = parts[-1]
            song = "by".join(parts[0:-1])

        if song_type == "next":
            resp = google_resp.next_song()
        elif song_type == "random":
            resp = google_resp.random_song()
        elif song and artist:
            resp = google_resp.search(song, artist)
        elif song and not artist:
            resp = google_resp.search(song)
        elif genre:
            resp = google_resp.song_by_genre(genre)

    return Response(resp, status=status.HTTP_200_OK, headers=NO_CACHE_HEADERS)
