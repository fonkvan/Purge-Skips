from auth import get_token
from artists import get_artist
import json

with open("settings.json") as settingsFile:
    settingsDict = json.load(settingsFile)
    dict = get_token(settingsDict)
    print(dict)
    fob = get_artist("https://api.spotify.com/v1/artists/4UXqAaa6dQYAk18Lv7PEgX?si=93rxZfMhTda_pmKBIT_M-Q", dict)
    print(fob)


