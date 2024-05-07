import requests

def get_token(settingsDict):
    id = settingsDict["client_id"]
    secret = settingsDict["secret"]
    token_dict = requests.post("https://accounts.spotify.com/api/token", data=f"grant_type=client_credentials&client_id={id}&client_secret={secret}", headers={"Content-Type": "application/x-www-form-urlencoded"})
    return token_dict.json()

