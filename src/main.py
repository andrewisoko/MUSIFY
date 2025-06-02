from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from oauth_spotify import OAuth_Spotify
import os
import urllib.parse
from fastapi.responses import Response



app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key= "to be added")
oauth = OAuth_Spotify()

@app.get("/")
async def frontend_msg():
       content = "Welcome to Musify<br>Please click the link to log in <a href='/login'>Spotify Log In</a>"
       return Response(content=content, media_type="text/html")

@app.get("/login")
async def login():
    scope = 'user-read-private user-read-email'
    params = {
        "client_id": os.getenv("CLIENT_ID"),
        "response_type": "code",
        "scope": scope,
        "redirect_uri": oauth.redirect_uri,
        "show_dialog": True
    }
    auth_url = f"{oauth.auth_url}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(auth_url)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
