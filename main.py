import auth
from artists import get_artist
import json
import playlist
import player

user_response = input("This application needs access to your web browser. Accept? ")
if user_response.upper() in ['YES', 'Y', 'YEAH', "YA", "YE"]:
    with open("settings.json") as settingsFile:
        settingsDict = json.load(settingsFile)
        queryparams = auth.req_user_auth(settingsDict)
        user_token_data = auth.get_token_auth_flow(settingsDict, queryparams)
        print(user_token_data)
        new_token = auth.refresh_token(user_token_data, settingsDict)
        print(new_token)
        #playback_state = player.get_playback_state(user_token_data["access_token"])
        #print(playback_state["actions"])
        #current_track = player.current_playing_track(user_token_data["access_token"])
        #artist_list = current_track["item"]["artists"]
        #artist = artist_list[0]["name"]
        #print(current_track["item"]["name"] + " by " + artist)
        #print(current_track["actions"])
        
