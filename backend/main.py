
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from oauth_spotify import OAuth_Spotify
import uvicorn



oauth = OAuth_Spotify()

origins = [
    "http://localhost:5173"
           ]

app = FastAPI(middleware=[Middleware(SessionMiddleware, secret_key="add key.")])
app.add_middleware(CORSMiddleware,
                   allow_origins = origins,
                   allow_credentials = True,
                   allow_methods = ["*"],
                   allow_headers = ["*"],
                   )


app.add_api_route("/", oauth.home, methods=["GET"])
app.add_api_route("/spot-login", oauth.spotify_login, methods=["GET"])
app.add_api_route("/callback", oauth.auth_response, methods=["GET"])
app.add_api_route("/playlists", oauth.get_playlists, methods=["GET"])
app.add_api_route("/tracks", oauth.get_tracks, methods=["GET"])
app.add_api_route("/refresh-token", oauth.refresh_token, methods=["GET"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)