from fastapi import FastAPI,Request
from fastapi.responses import RedirectResponse,JSONResponse
import requests
import os
from datetime import datetime
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv



class OAuth_Spotify():
    
   
    
    app = FastAPI()

        
    def spotify_urls(self):
        
        self.url_account_apitoken ="https://accounts.spotify.com/api/token"
        self.redirect_uri = "http://127.0.0.1:8888/callback"
        self.auth_url ="https://accounts.spotify.com/authorize"
        self.baseapi_url ="https://api.spotify.com/v1/"
        
    
    
    @app.route("/callback")
    
    async def callback(self):
        
        request = Request()
        load_dotenv(dotenv_path="src/.env")
        
        if 'error' in request.query_params:
            return {"error":request.query_params['error']}
        
        elif 'code' in request.query_params:
            request_body = {
                'code': request.query_params['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.redirect_uri,
                'client_id':  os.getenv("CLIENT_ID"),
                'client_secret': os.getenv("CLIENT_SECRET"),  
            }
            
            response = requests.post(self.url_account_apitoken, data=request_body)
            token_json_info= response.json()
            
            request.session['access_token'] = token_json_info['access_token']
            request.session['refresh_token']  = token_json_info['refresh_token']
            request.session['expires_at'] = datetime.now().timestamp() + token_json_info['expires_in']
            
            return RedirectResponse('/playlists')
    
    
     
     
    @app.route('/playlists')       
            
    async def get_playlists(self,session : Request):
        
        if 'access_token' not in session:
            return RedirectResponse(url="/login")

        elif datetime.now().timestamp() > session.get('expires_at', 0):
            return RedirectResponse(url="/refresh-token")
        
        headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
        response = requests.get(self.baseapi_url + 'me/playlists', headers=headers)
        playlists = response.json()
        
        return JSONResponse(content=playlists)
    
    

    @app.route('/refresh-token')       
            
    async def refresh_token(self,request: Request):  
        
        refresh_token = request.session.get('refresh_token')
        
        if not refresh_token:
            return RedirectResponse("/login")
        
        elif datetime.now().timestamp() > request.session.get('expires_at', 0):
            
            request_body = {
        
                'grant_type': 'refresh_token',
                'refresh_token': request.session['refresh_token'],
                'client_id':  os.getenv("CLIENT_ID"),
                'client_secret': os.getenv("CLIENT_SECRET"),  
            }
            
            response = requests.post(url=self.url_account_apitoken,data=request_body)
            new_token_json_info = response.json()
            
            request.session["access_token"] = new_token_json_info["access_token"]
            request.session['expires_at'] = datetime.now().timestamp() + new_token_json_info['expires_in']
            
            
            return RedirectResponse("/playlists")
        

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)     
        