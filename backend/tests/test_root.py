from fastapi.testclient import TestClient
from backend.main import app 
import urllib.parse
import os


### to run the test change the main.py modules in relative paths ex: from backend.oauth_spotify import OAuth_Spotify, from  backend.youtube_downloader import *  etc...

client = TestClient(app)


def test_read_root():
    
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "Welcome to Musify"



        
    
    
      
    

    

    
    