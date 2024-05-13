from common import common_get

def get_artist(url, token):
    artist_dict = common_get(url, token)
    return artist_dict.json()

