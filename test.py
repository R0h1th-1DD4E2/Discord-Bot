import os
from dotenv import load_dotenv
import requests
import random
import string
import base64

load_dotenv()
client_secret = os.getenv('client_secret')
client_id = os.getenv('client_id')
code = os.getenv('SPOTIFY_CODE')

redirect_uri = 'http://localhost:8888/callback'
state = ''.join(random.choices(string.ascii_lowercase , k=16))
base_url = "https://accounts.spotify.com"
encoded_cred = base64.b64encode((client_id + ":" + client_secret).encode()).decode("utf-8")
reference_url = "https://api.spotify.com/v1"

def user_auth():
    auth_link = base_url + "/authorize"
    query_params = {
        "client_id" : client_id,
        "response_type" : "code",
        "redirect_uri" : redirect_uri,
        "scope" : 'user-read-private user-read-email',
        "state": state
    }
    authorization_url = auth_link + '?' + '&'.join([f'{k}={v}' for k, v in query_params.items()])
    return authorization_url

def access_token():
    token_link = base_url + "/api/token"
    header_params = {
        'Authorization' : "Basic " + encoded_cred,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body_params = {
        "grant_type" : "authorization_code",
        "code" : code,
        "redirect_uri" : redirect_uri
    }

    data = requests.post(token_link, headers=header_params, data=body_params)
    if data.status_code == 200:
        response = data.json()
        final_token = response['access_token']
    else:
        print(data, "Try again :(")

def search():
    search_url = reference_url + "/search"
    header_params = {
        "Authorization" : "Bearer " + access_token,
    }
    params = {
        "q" : "high on life",
        "type" : "track"
    }
    data = requests.get(search_url, headers=header_params, params=params)
    if data.status_code == 200:
        response = data.text
        write.json_write(response)
        response = data.json()
        print(response["tracks"]["items"][0]["external_urls"]['spotify'])


search()