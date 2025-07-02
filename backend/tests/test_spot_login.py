from fastapi.testclient import TestClient
from fastapi import FastAPI
from backend.main import app 
from dotenv import load_dotenv
from backend.oauth_spotify import OAuth_Spotify
import urllib.parse
import os
import base64
import requests

### to run the test change the main.py modules in relative paths ex: from backend.oauth_spotify import OAuth_Spotify, from  backend.youtube_downloader import *  etc...


client = TestClient(app)



# scope = 'playlist-read-collaborative'
# scope1 = playlist-read-private
# scope2 = 'playlist-modify-private'
# scope3 = 'playlist-modify-public'

def test_read_spot_login():
    
    
    
    auth_url = "https://accounts.spotify.com/authorize"
    redirect_uri = "http://127.0.0.1:8888/callback"
    scope = 'playlist-read-collaborative'
    
    params = {
        "client_id":"client",
        "response_type": "code",
        "scope": scope,
        "redirect_uri": redirect_uri,
        "show_dialog": True
    }
    auth_url_redirect = f"{auth_url}?{urllib.parse.urlencode(params)}"  # To fix
    
    response_statuscode = client.get("/spot-login", follow_redirects=False)
    assert response_statuscode.status_code == 307

       
       


def test_client_id():
    
    """testing client id with invalid value"""
    
    app_clientId = FastAPI()
    oauth = OAuth_Spotify()
    
    oauth.client_id = ""

    app_clientId.add_api_route("/spot-login", oauth.spotify_login, methods=["GET"])
    client_for_clientid = TestClient(app_clientId)
    
    response = client_for_clientid.get("/spot-login")
    
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Client id missing or invalid, please check."
    }
    
    

    

def test_no_scope():
    
    """testing scopes with invalid value"""
    
    load_dotenv("backend/.env")   
    
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    user_id = os.getenv("USER_ID")


    credentials = f"{client_id}:{client_secret}"
    credentials_b64 = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {credentials_b64}",
        "Content-Type": "application/x-www-form-urlencoded",
        "scope":'playlist-read-collaborative'
    }
    data = {
        "grant_type": "client_credentials"
    }
    
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    access_token = response.json()['access_token']
   

    spotify_playlists_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers_playlist = {'Authorization': f"Bearer {access_token}"}
    
    response = requests.get(spotify_playlists_url,
                            headers=headers_playlist,
                            params={"limit": 50})
    
    playlist = response.json()
    total_playlist = playlist['total']
    
    assert total_playlist == 4
    
    
    
    
    
    
    

    



    
    # .env commented or wrong client id = INVALID_CLIENT: Invalid client
    
    # Scope = if "" should return  4 playlists
    
    # Wrong redirect uri = Illegal redirect_uri
    
    # empty redirect uri = Missing required parameter: redirect_uri
