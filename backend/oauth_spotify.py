from fastapi import Request,HTTPException
from fastapi.responses import Response, RedirectResponse, JSONResponse
import httpx
import os
from pathlib import Path
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
        self.scope = 'playlist-read-collaborative'
        self.url_getplaylist = None
        self.playlists = None
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.directory_path = os.path.abspath(__file__)
        self.parent_directory = os.path.dirname(self.directory_path)
        self.grandparent_dir = os.path.dirname(self.parent_directory)
        self.cache_lifespan = 3600
 
    
    
    
    async def home(self):
        
        """The first page from local address, provides the spotify login page link"""
        
        content = "Welcome to Musify"
        return Response(content=content)
    
    

    async def spotify_login(self): #removed request parameter check later.
        
        """Redirect the user to the auth url."""
        
        if self.client_id == "":
            raise HTTPException(status_code=400, detail="Client id missing or invalid, please check.") 
        else:
            params = {
                "client_id":f"{self.client_id}",
                "response_type": "code",
                "scope": self.scope,
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
        
        cache_path = Path("playlists_cache.json")
        
        # if data exists json data cache exists it will be accessed for an hour.
        
        if cache_path.exists() and (time.time() - cache_path.stat().st_mtime < self.cache_lifespan):
            with open(cache_path, "r") as f:
                self.playlists = json.load(f)
                print("Using current playlist cache")
             
            return JSONResponse(content=self.playlists)
        
        if 'access_token' not in request.session:
            return RedirectResponse(url="/spot-login")
            
        elif datetime.now().timestamp() > request.session.get('expires_at', 0):
            return RedirectResponse(url="/refresh-token")
        
        
        else:
            headers = {'Authorization': f"Bearer {request.session['access_token']}"}
            async with httpx.AsyncClient() as client:
                response = await client.get(self.baseapi_url, headers=headers,params={"limit": 50})
                
               #After the first request the data gets stored in a json file to avoid too many API calls.
                try:
                    self.playlists = response.json()
                    with open(cache_path, "w") as f:
                      json.dump(self.playlists, f,indent=4)
                      print(f"playlist json file generated at {time.ctime(cache_path.stat().st_mtime)}")
                    
                    
                except Exception as err:
                    print("Status code:", response.status_code, {err})
                    print("Response content:", response.text)
                    
        return JSONResponse(content=self.playlists)
    
    

    async def get_tracks(self, request: Request):
    
        """Returns a list of all tracks in a playlist"""
        
        cache_file_path = Path(self.grandparent_dir, "frontend", "public","services","allTracks.json")
        
        with open ("playlists_cache.json","r") as file:
            playlist_cache = json.load(file)
        
        # Return cached data if file exists and is recent (e.g., <1 hour old)
        if cache_file_path.exists() and (time.time() - cache_file_path.stat().st_mtime < self.cache_lifespan):
            with open(cache_file_path) as f:
                print("Using current all_tracks cache")
                return JSONResponse(content=json.load(f))

        else:
            playlists_data = playlist_cache
            json_trial_list = []
            for playlist in playlists_data["items"]:
                playlist_name = playlist["name"]
                playlists_id = playlist["id"]
                self.url_getplaylist = f"https://api.spotify.com/v1/playlists/{playlists_id}"

                headers = {"Authorization": f"Bearer {request.session['access_token']}"}
                async with httpx.AsyncClient() as client:
                    playlist_request = await client.get(url=self.url_getplaylist, headers=headers)
                    
                    try:
                     single_playlist = playlist_request.json()
                    except Exception as err:
                        print("Status code:", playlist_request.status_code)
                        print("Response content:", playlist_request.text)

                track_info = []
                track_items = single_playlist["tracks"]["items"]
                for track_dict in track_items:
                    artist_name = track_dict["track"]["album"]["artists"][0]["name"]
                    track_name = track_dict["track"]["name"]
                    track_info.append(f'{artist_name} {track_name}')
                json_trial_list.append({playlist_name: track_info})
            dump_path = os.path.join(self.grandparent_dir,"frontend","public","services")
            
            with open(f"{dump_path}/allTracks.json", "w") as file:
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
        