import requests

def get_artist(url, tokenDict):
    token = tokenDict["access_token"]
    auth = tokenDict["token_type"]
    header = {"Authorization" : f"{auth} {token}"}
    artist_dict = requests.get(url, headers=header)
    return artist_dict.json()

