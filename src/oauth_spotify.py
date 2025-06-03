from fastapi import Request
from fastapi.responses import Response, RedirectResponse, JSONResponse
import requests
import os
from datetime import datetime
import urllib.parse
from dotenv import load_dotenv




class OAuth_Spotify:
    
    """all the accessible urls are contanied in the contstructor."""
    
    def __init__(self):
        self.url_account_apitoken = "https://accounts.spotify.com/api/token"
        self.redirect_uri = "http://127.0.0.1:8888/callback"
        self.auth_url = "https://accounts.spotify.com/authorize"
        self.baseapi_url = "https://api.spotify.com/v1/"
    
    
    async def home(self):
        
        """The first page from local address, provides the spotify login page link"""
        
        content = "Welcome to Musify<br>Please click the link to log in <a href='/login'>Spotify Log In</a>"
        return Response(content=content, media_type="text/html")
    
    

    async def login(self, request: Request):
        
        """Redirect the user to the auth url."""
        
        load_dotenv(dotenv_path="src/.env")
        scope = 'user-read-private user-read-email'
        params = {
            "client_id": os.getenv("CLIENT_ID"),
            "response_type": "code",
            "scope": scope,
            "redirect_uri": self.redirect_uri,
            "show_dialog": True
        }
        auth_url = f"{self.auth_url}?{urllib.parse.urlencode(params)}"
        return RedirectResponse(auth_url)
    
    

    async def callback(self, request: Request):
        
        """Post recquest to the api token url and redirecting to playlist endpoint."""
        
        load_dotenv(dotenv_path="src/.env")
        if 'error' in request.query_params:
            return {"error": request.query_params['error']}
        
        elif 'code' in request.query_params:
            request_body = {
                'code': request.query_params['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.redirect_uri,
                'client_id': os.getenv("CLIENT_ID"),
                'client_secret': os.getenv("CLIENT_SECRET"),  
            }
            response = requests.post(self.url_account_apitoken, data=request_body)
            token_json_info = response.json()
            request.session['access_token'] = token_json_info['access_token']
            request.session['refresh_token'] = token_json_info['refresh_token']
            request.session['expires_at'] = datetime.now().timestamp() + token_json_info['expires_in']
    
            return RedirectResponse('/playlists')



    async def get_playlists(self, request: Request):
        
        """Playlist displayed as json document."""
        
        if 'access_token' not in request.session:
            return RedirectResponse(url="/login")
        
        elif datetime.now().timestamp() > request.session.get('expires_at', 0):
            return RedirectResponse(url="/refresh-token")
        
        headers = {'Authorization': f"Bearer {request.session['access_token']}"}
        response = requests.get(self.baseapi_url + 'me/playlists', headers=headers)
        playlists = response.json()
        return JSONResponse(content=playlists)



    async def refresh_token(self, request: Request):
        
        """Handles expired refrsh token by providing new tokens if the latter is expired, for then redirecting to the playlist endpoint."""
        
        refresh_token = request.session.get('refresh_token')
        
        if not refresh_token:
            return RedirectResponse("/login")
        
        elif datetime.now().timestamp() > request.session.get('expires_at', 0):
            request_body = {
                'grant_type': 'refresh_token',
                'refresh_token': request.session['refresh_token'],
                'client_id': os.getenv("CLIENT_ID"),
                'client_secret': os.getenv("CLIENT_SECRET"),  
            }
            response = requests.post(url=self.url_account_apitoken, data=request_body)
            new_token_json_info = response.json()
            request.session["access_token"] = new_token_json_info["access_token"]
            request.session['expires_at'] = datetime.now().timestamp() + new_token_json_info['expires_in']
            return RedirectResponse("/playlists")