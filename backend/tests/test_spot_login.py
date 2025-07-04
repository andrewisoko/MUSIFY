from fastapi.testclient import TestClient
from fastapi import FastAPI
from backend.main import app 
from dotenv import load_dotenv
from backend.oauth_spotify import OAuth_Spotify
import urllib.parse
import os


### to run the test change the main.py modules in relative paths ex: from backend.oauth_spotify import OAuth_Spotify, from  backend.youtube_downloader import *  etc...


client = TestClient(app)



def test_read_spot_login():
    

    auth_url = "https://accounts.spotify.com/authorize"
    redirect_uri = "http://127.0.0.1:8888/callback"
    scope = 'playlist-read-collaborative'
    
    params = {
        "client_id": None,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": redirect_uri,
        "show_dialog": True
    }
    auth_url_redirect = f"{auth_url}?{urllib.parse.urlencode(params)}" 
    
    response_statuscode = client.get("/spot-login", follow_redirects=False)
    assert response_statuscode.status_code == 307
    assert response_statuscode.headers["location"] == auth_url_redirect

       
       
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
    
    

    
    
    
    
    
    
    
    

    



    
    # .env commented or wrong client id = INVALID_CLIENT: Invalid client
    
    # Scope = if "" should return  4 playlists
    
    # Wrong redirect uri = Illegal redirect_uri
    
    # empty redirect uri = Missing required parameter: redirect_uri
