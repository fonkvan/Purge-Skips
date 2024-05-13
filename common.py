import requests
import base64

def common_get(url, token):
    return requests.get(url, headers={"Authorization" : f"Bearer {token}"})

def encode_client_info(settingsDict):
    client_id_and_secret = f"{settingsDict["client_id"]}:{settingsDict["secret"]}"
    return base64.b64encode(client_id_and_secret.encode())

