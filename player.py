from common import common_get

PLAYER_URL = "https://api.spotify.com/v1/me/player"

def get_playback_state(token):
    playback_state = common_get(PLAYER_URL, token)
    return playback_state.json()

def current_playing_track(token):
    URL = f"{PLAYER_URL}/currently-playing"
    current_track = common_get(URL, token)
    return current_track.json()


