from fastapi import Request
from fastapi.responses import Response, RedirectResponse, JSONResponse
import httpx
import os
from datetime import datetime
import urllib.parse
from dotenv import load_dotenv
import json
import time
import requests




class OAuth_Spotify:
    
    """all the accessible urls are contanied in the contstructor."""
    
    def __init__(self):
        
        load_dotenv(".env")
        self.url_account_apitoken = "https://accounts.spotify.com/api/token"
        self.redirect_uri = "http://127.0.0.1:8888/callback"
        self.auth_url = "https://accounts.spotify.com/authorize"
        self.baseapi_url = "https://api.spotify.com/v1/me/playlists"
        self.url_getplaylist = None
        self.playlists = None
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
    
    
    
    async def home(self):
        
        """The first page from local address, provides the spotify login page link"""
        
        content = "Welcome to Musify<br>Please click the link to log in <a href='/spot-login'>Spotify Log In</a>"
        return Response(content=content, media_type="text/html")
    
    

    async def spotify_login(self, request: Request):
        
        """Redirect the user to the auth url."""
        
        load_dotenv(".env")
        scope = 'playlist-read-collaborative'
        params = {
            "client_id":f"{self.client_id}",
            "response_type": "code",
            "scope": scope,
            "redirect_uri": self.redirect_uri,
            "show_dialog": True
        }
        auth_url = f"{self.auth_url}?{urllib.parse.urlencode(params)}"
        return RedirectResponse(auth_url)
    
    

    async def auth_response(self, request: Request):
        
        """Post recquest to the api token url and redirecting to playlist endpoint."""
        
        
        if 'error' in request.query_params:
            return {"error": request.query_params['error']}
        
        elif 'code' in request.query_params:
            request_body = {
                'code': request.query_params['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.redirect_uri,
                'client_id':f"{self.client_id}",
                'client_secret':f"{self.client_secret}",  
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(self.url_account_apitoken, data=request_body)
                token_json_info = response.json()
                request.session['access_token'] = token_json_info['access_token']
                request.session['refresh_token'] = token_json_info['refresh_token']
                request.session['expires_at'] = datetime.now().timestamp() + token_json_info['expires_in']
            
            return RedirectResponse('http://127.0.0.1:5173/playlists')



    async def get_playlists(self, request: Request):
        
        """Playlist displayed as json document."""
        
        
        if 'access_token' not in request.session:
            return RedirectResponse(url="/spot-login")
        
        elif datetime.now().timestamp() > request.session.get('expires_at', 0):
            return RedirectResponse(url="/refresh-token")
        
        headers = {'Authorization': f"Bearer {request.session['access_token']}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(self.baseapi_url, headers=headers,params={"limit": 50})
            self.playlists = response.json()
           
        return JSONResponse(content=self.playlists)
    
    

    async def get_tracks(self, request: Request):
        playlists_data = self.playlists
        json_trial_list = []
        for playlist in playlists_data["items"]:
            playlist_name = playlist["name"]
            playlists_id = playlist["id"]
            self.url_getplaylist = f"https://api.spotify.com/v1/playlists/{playlists_id}"

            headers = {"Authorization": f"Bearer {request.session['access_token']}"}
            async with httpx.AsyncClient() as client:
                playlist_request = await client.get(url=self.url_getplaylist, headers=headers)
                single_playlist = playlist_request.json()

            track_info = []
            track_items = single_playlist["tracks"]["items"]
            for track_dict in track_items:
                artist_name = track_dict["track"]["album"]["artists"][0]["name"]
                track_name = track_dict["track"]["name"]
                track_info.append(f'{artist_name} {track_name}')
            json_trial_list.append({playlist_name: track_info})

        with open("all_tracks.json", "w") as file:
            json.dump(json_trial_list, file, indent=4)

        return JSONResponse(content=json_trial_list)

        
        
        
    async def refresh_token(self, request: Request):
        
        """Handles expired refrsh token by providing new tokens if the latter is expired, for then redirecting to the playlist endpoint."""
        
        refresh_token = request.session.get('refresh_token')
        
        if not refresh_token:
            return RedirectResponse("/spot-login")
        
        elif datetime.now().timestamp() > request.session.get('expires_at', 0):
            request_body = {
                'grant_type': 'refresh_token',
                'refresh_token': request.session['refresh_token'],
                'client_id':f"{self.client_id}",
                'client_secret':f"{self.client_secret}",  
            }
            async with httpx.AsyncClient() as client:
                
                response = await client.post(url=self.url_account_apitoken, data=request_body)
                new_token_json_info = response.json()
                request.session["access_token"] = new_token_json_info["access_token"]
                request.session['expires_at'] = datetime.now().timestamp() + new_token_json_info['expires_in']
            return RedirectResponse("/playlists")
        