import requests
import string
import random
import webbrowser
import urllib, urllib.parse
from sys import exit
from common import encode_client_info
from enum import Enum

class Flow(Enum):
    NONE = 0
    AUTH = 1
    CLIENT_CREDS = 2
    PKCE = 3

flow = Flow.NONE

URL = "https://accounts.spotify.com/api/token"
R_URI ="http://localhost/"
URLENCODED = "application/x-www-form-urlencoded"

def req_user_auth(settingsDict):
    id = settingsDict["client_id"]
    state = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    scope = settingsDict["scope"]
    params = {'response_type':'code', 'client_id':id, 'scope':scope, 'redirect_uri':R_URI, 'state':state}
    auth_url = "https://accounts.spotify.com/authorize?"
    final_url = "{}{}".format(auth_url, urllib.parse.urlencode(params))
    webbrowser.open(final_url)
    #ideally would capture redirect but not sure how to do that at the moment and couldn't find good resources
    #for now just ask user for redirect uri to confirm and parse
    user_uri = input("""Please copy and paste entire URL that you were redirected to upon accepting request from app. 
Note that it is common to see \'This site can\'t be reached\' in your web browser. """)
    parsed_url = urllib.parse.urlparse(user_uri)
    queryparams = urllib.parse.parse_qs(parsed_url.query)
    if queryparams['state'][0] != state:
        print("State does not match. Authentication flow rejected")
        exit()
    if "error" in queryparams:
        print("Error")
        exit()
    return queryparams
    
def get_token_auth_flow(settingsDict, queryparams):
    code = queryparams['code'][0]
    state = queryparams['state'][0]
    client_id_and_secret_64 = encode_client_info(settingsDict)
    if state is None:
        print("state is None")
        exit()
    else:
        response = requests.post(URL, data=f"grant_type=authorization_code&code={code}&redirect_uri={R_URI}",
                      headers={"content-type":URLENCODED,"Authorization":f"Basic {client_id_and_secret_64.decode()}"})
        rjson = response.json()
        if "error" in rjson:
            print("ERROR")
            print(rjson)
            exit()
        print("SUCCESS")
        global flow 
        flow = Flow.AUTH
        return rjson


def get_token_client_creds(settingsDict):
    id = settingsDict["client_id"]
    secret = settingsDict["secret"]
    token_dict = requests.post(URL, data=f"grant_type=client_credentials&client_id={id}&client_secret={secret}", headers={"Content-Type": URLENCODED})
    global flow 
    flow = Flow.CLIENT_CREDS
    return token_dict.json()

#should probably be called async, but need to be careful sense refreshing token could make access_token invalid
def refresh_token(old_token, settingsDict):
    match flow:
        case Flow.AUTH:
            print("Auth flow refresh")
            return refresh_auth_flow(old_token, settingsDict)
        case Flow.CLIENT_CREDS:
            print("Cannot refresh token with client credentials")
            return old_token
        case Flow.PKCE:
            print("PKCE refresh")
            return refresh_pkce(old_token, settingsDict)

def refresh_auth_flow(old_token, settingsDict):
    refresh_token = old_token["refresh_token"]
    client_id_and_secret_64 = encode_client_info(settingsDict)
    response = requests.post(URL, data=f"grant_type=refresh_token&refresh_token={refresh_token}", headers={"Content-Type" : URLENCODED, "Authorization":f"Basic {client_id_and_secret_64.decode()}"})
    rjson = response.json()
    if "error" in rjson:
        print("Could not refresh token")
        print(rjson)
        exit()
    print("Token refreshed.")
    return rjson

#TODO:
def refresh_pkce(old_token, settingsDict):
    global flow 
    flow = Flow.PKCE
    return

