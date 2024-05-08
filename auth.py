import requests
import string
import random
import webbrowser
import urllib, urllib.parse
from sys import exit
import base64

URL = "https://accounts.spotify.com/api/token"
R_URI ="http://localhost/"
URLENCODED = "application/x-www-form-urlencoded"

def req_user_auth(settingsDict):
    id = settingsDict["client_id"]
    state = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    scope = 'user-read-private user-read-email'
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
    client_id_and_secret = f"{settingsDict["client_id"]}:{settingsDict["secret"]}"
    client_id_and_secret_64 = base64.b64encode(client_id_and_secret.encode())
    client_id_64 = base64.b64encode(settingsDict['client_id'].encode())
    secret_64 = base64.b64encode(settingsDict['secret'].encode())
    if state is None:
        print("state is None")
        exit()
    else:
        response = requests.post(URL, data=f"grant_type=authorization_code&code={code}&redirect_uri={R_URI}",
                      headers={"content-type":URLENCODED,"Authorization":f"Basic {client_id_and_secret_64.decode()}"})
        if "error" in response.json():
            print("ERROR")
            print(response.json())
            exit()
        print("SUCCESS")
        return response.json()


def get_token_client_creds(settingsDict):
    id = settingsDict["client_id"]
    secret = settingsDict["secret"]
    token_dict = requests.post(URL, data=f"grant_type=client_credentials&client_id={id}&client_secret={secret}", headers={"Content-Type": URLENCODED})
    return token_dict.json()

#TODO:
def refresh_token(settingsDict):
    id = settingsDict["client_id"]
    token_dict = requests.post(URL, data=f"grant_type=refresh_token&client_id={id}")

