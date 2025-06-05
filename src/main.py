
from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from oauth_spotify import OAuth_Spotify
import uvicorn


app = FastAPI(middleware=[Middleware(SessionMiddleware, secret_key="generate personal key. As long as it is a string it will be valid.")])
oauth = OAuth_Spotify()

app.add_api_route("/", oauth.home, methods=["GET"])
app.add_api_route("/login", oauth.login, methods=["GET"])
app.add_api_route("/callback", oauth.auth_response, methods=["GET"])
app.add_api_route("/playlists", oauth.get_playlists, methods=["GET"])
app.add_api_route("/tracks", oauth.get_tracks, methods=["GET"])
app.add_api_route("/refresh-token", oauth.refresh_token, methods=["GET"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)