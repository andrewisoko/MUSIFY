from fastapi.testclient import TestClient
from backend.main import app 
from backend.oauth_spotify import OAuth_Spotify
from dotenv import load_dotenv
import urllib.parse
import os
from fastapi.responses import RedirectResponse

### to run the test change the main.py modules in relative paths ex: from backend.oauth_spotify import OAuth_Spotify, from  backend.youtube_downloader import *  etc...

client = TestClient(app)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "Welcome to Musify"


def test_read_spot_login():

    response = client.get("/spot-login", follow_redirects=False)
    assert response.status_code == 307 

    

    
    