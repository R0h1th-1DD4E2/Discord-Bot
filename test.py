import os
from dotenv import load_dotenv
import requests
import random
import string
import base64
import json_handler
import webbrowser

load_dotenv()
client_secret = os.getenv('client_secret')
client_id = os.getenv('client_id')
first_code = os.getenv('SPOTIFY_CODE')

redirect_uri = 'http://localhost:8888/callback'
state = ''.join(random.choices(string.ascii_lowercase , k=16))
base_url = "https://accounts.spotify.com"
encoded_cred = base64.b64encode((client_id + ":" + client_secret).encode()).decode("utf-8")
reference_url = "https://api.spotify.com/v1"

access_time, expire_date, access_key, refresh_token = json_handler.load_json()

code = refresh_token if refresh_token is not None else first_code

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
        json_handler.dump_json(response)
        print("Success!!! writing to file")
    else:
        print(f"Server responed with {data.status_code}, Try again :(")

def search(to_search , search_type):
    search_url = reference_url + "/search"
    header_params = {
        "Authorization" : "Bearer " + access_key,
    }
    params = {
        "q" : to_search,
        "type" : search_type
    }
    data = requests.get(search_url, headers=header_params, params=params)
    if data.status_code == 200:
        response = data.text
        response = data.json()
        print(response["tracks"]["items"][0]["external_urls"]['spotify'])


# webbrowser.open(user_auth())
# access_token()
search("in the name of love", "track")