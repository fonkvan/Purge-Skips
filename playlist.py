from common import common_get

URL = "https://api.spotify.com/v1/playlists/"

def get_playlist(token, id):
    final_url = f"{URL}{id}"
    playlist = common_get(final_url, token)
    return playlist.json()

