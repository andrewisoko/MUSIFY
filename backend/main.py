from fastapi import FastAPI
from fastapi.responses import FileResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from backend.oauth_spotify import OAuth_Spotify
import uvicorn
from backend.youtube_downloader import * 
from backend.delete_it import *
from pydantic import BaseModel
import shutil
from fastapi.testclient import TestClient
from fastapi import FastAPI

def test_client_id():
    # 1. Create a NEW FastAPI app instance for this test
    app = FastAPI()
    
    # 2. Initialize your OAuth object
    oauth = OAuth_Spotify()
    oauth.client_id = ""
    oauth.auth_url = "https://accounts.spotify.com/authorize"
    oauth.redirect_uri = "http://127.0.0.1:8888/callback"
    
    # 3. Register the route with THIS app instance
    app.add_api_route("/spot-login", oauth.spotify_login, methods=["GET"])
    
    # 4. Create TestClient AFTER registering routes
    client = TestClient(app)
    
    # 5. Make the request
    response = client.get("/spot-login")
    
    # 6. Validate
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Client id missing or invalid, please check."
    }

origins = [
    "http://127.0.0.1:5173",
]

#-------------------------------------------------------------------------------------------------------

app = FastAPI()
downloader = YoutubeDownloader()  
oauth = OAuth_Spotify()
cleanup = DeleteIt()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=""
)
#--------------------------------------------------------------------------------------------------

class PlaylistRequest(BaseModel):
    
    """Needed to retrieve the playlist name from the frontend."""
    playlist_name: str
    
class DeletePlaylistRequest(BaseModel):
    
    """Needed to retrieve the playlist name from the frontend."""
    playlist_name: str
    
class DeleteZipPlaylist(BaseModel):
    
    """Needed to retrieve the zip playlist name from the frontend."""
    playlist_name: str
    
class AudioData(BaseModel):
    
    """Audio url from frontend."""
    
    audio_url: str
    
  
  
    
        
 
#--------------------------------------------------------------------------------------------------

#Creating and deleting playlist from the directory.

@app.post("/download-playlist")
async def download_playlist(plst_name:PlaylistRequest):
    
    """As the post request gets triggered the the playlist folder gets generated into the directory."""
    
    downloader.retrieve_playlists()
    result = downloader.download_selected_playlist(plst_name.playlist_name)
    return {"message": result}


@app.post("/delete-playlist")
def delete_playlist_intime(plst_name:DeletePlaylistRequest):
    time.sleep(30)
    cleanup.delete_playlistsdirectory(plst_name.playlist_name)
    
    return "Playlist deleted."


#----------------------------------------------------------------------------------------------------


#Creating and deleting zip playlist from the directory.

@app.get("/api/download/{playlist_name}")
def download_playlist_zipfile(playlist_name: str):

    """It generates a zip file for the downloading from the browser."""
    
    current_dir = os.path.abspath(__file__)
    backend_dir = os.path.dirname(current_dir)

    downloads_path = os.path.join(backend_dir,"Playlists downloads",playlist_name,"downloads")
    zip_path = os.path.join(backend_dir,"zip playlist", f"{playlist_name}.zip")

    if not os.path.exists(downloads_path):
        return {"error": f"No downloads folder found for this playlist: {downloads_path}"}

    elif os.path.exists(zip_path):
        os.remove(zip_path)
        print(f"Old ZIP removed: {zip_path}")

    shutil.make_archive(os.path.splitext(zip_path)[0], 'zip', downloads_path)

    if not os.path.exists(zip_path):
        return {"error": "ZIP file could not be created."}
    
    return FileResponse(
        zip_path,
        filename=f"{playlist_name}.zip",
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={playlist_name}.zip"}
    )


@app.post("/delete-zipplaylist")
async def delete_zipplaylist_intime(zip_name:DeleteZipPlaylist):
    
    time.sleep(10)
    cleanup.delete_zipplaylist(zip_name.playlist_name)
    
    return "Zip playlist deleted."
    
    
#----------------------------------------------------------------------------------------------------- 


@app.post("/download-audio")
async def audio_download(audio_data:AudioData):
    result = downloader.download_from_yt_link(audio_data.audio_url)
    return result
 
 
@app.get("/0101delete-audio")
def delete_audio_intime():
    
    time.sleep(200)
    cleanup.delete_audio_dir()
    
    return "Yt audio deleted."
 

#-----------------------------------------------------------------------------------------------------

@app.get("/download-zipaudio")  
async def download_audio_zip():
    current_dir = os.path.abspath(__file__)
    backend_dir = os.path.dirname(current_dir)

    downloads_path = os.path.join(backend_dir,"Youtube Downloads","downloads")
    zip_path = os.path.join(backend_dir,"Youtube Downloads.zip")
    
    shutil.make_archive(os.path.splitext(zip_path)[0], 'zip', downloads_path)
    try:
        return FileResponse(
            zip_path,
            filename="Youtube Downloads.zip",
            media_type="application/zip",
            headers={"Content-Disposition":"attachment; filename=Youtube Downloads.zip"})
    except:
        return JSONResponse("Zip file not Generated")
 

@app.get("/delete-zipaudio")
def delete_zipaudio_intime():
    
    time.sleep(200)
    cleanup.delete_audiozip()
    
    return "Yt zip audio deleted."
     
#-----------------------------------------------------------------------------------------------------

app.add_api_route("/", oauth.home, methods=["GET"])
app.add_api_route("/spot-login", oauth.spotify_login, methods=["GET"])
app.add_api_route("/callback", oauth.auth_response, methods=["GET"])
app.add_api_route("/playlists", oauth.get_playlists, methods=["GET"])
app.add_api_route("/tracks", oauth.get_tracks, methods=["GET"])
app.add_api_route("/refresh-token", oauth.refresh_token, methods=["GET"])

if __name__ == "__main__":
    
    print(cleanup.delete_all()) #deletes previous items created.
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
