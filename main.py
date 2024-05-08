from auth import *
from artists import get_artist
import json

user_response = input("This application needs access to your web browser. Accept? ")
if user_response.upper() in ['YES', 'Y', 'YEAH', "YA", "YE"]:
    with open("settings.json") as settingsFile:
        settingsDict = json.load(settingsFile)
        queryparams = req_user_auth(settingsDict)
        user_token_data = get_token_auth_flow(settingsDict, queryparams)
        print(user_token_data)
        #dict = get_token(settingsDict)
        #fob = get_artist("https://api.spotify.com/v1/artists/4UXqAaa6dQYAk18Lv7PEgX?si=93rxZfMhTda_pmKBIT_M-Q", dict)

