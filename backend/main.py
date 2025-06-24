from fastapi import FastAPI
import zipfile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from oauth_spotify import OAuth_Spotify
import uvicorn
from  youtube_downloader import * 
from pydantic import BaseModel
import shutil


origins = [
    "http://127.0.0.1:5173",
]

#-------------------------------------------------------------------------------------------------------

app = FastAPI()
downloader = YoutubeDownloader()  
oauth = OAuth_Spotify()

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
        
 
#--------------------------------------------------------------------------------------------------

#Creating and deleting playlist from the directory.

@app.post("/download-playlist")
async def download_playlist(plst_name:PlaylistRequest):
    
    """As the post request gets triggered the the playlist folder gets generated into the directory."""
    downloader.retrieve_playlists()
    result = downloader.download_selected_playlist(plst_name.playlist_name)
    return {"message": result}

app.add_api_route("/delete-playlist", downloader.delete_playlist, methods=["GET"])


#----------------------------------------------------------------------------------------------------


#Creating and deleting zip playlist from the directory.

@app.get("/api/download/{playlist_name}")
def download_playlist_zipfile(playlist_name: str):

    """It generates a zip file for the downloading from the browser."""
    
    current_dir = os.path.abspath(__file__)
    backend_dir = os.path.dirname(current_dir)

    downloads_path = os.path.join(backend_dir,playlist_name,"downloads")
    zip_path = os.path.join(backend_dir, f"{playlist_name}.zip")

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


@app.get("/delete-zipplaylist")
def delete_zipplaylist(playlist_name:str):
    
    """Deletes zip playlist from directory after 10 minutes."""
    
    current_dir = os.path.abspath(__file__)
    backend_dir = os.path.dirname(current_dir)
    
    zip_path = os.path.join(backend_dir,f"{playlist_name}.zip")
    
    if os.path.exists(zip_path):
        
        time.sleep(600)
        with open(zip_path, "rb") as file:
            playlist_zip_file = zipfile.ZipFile(file)
            for items in playlist_zip_file.namelist():
                filename = os.path.basename(items)
                if not filename:
                    continue
                else:
                   source = playlist_zip_file.open(items)
        os.remove(zip_path)
    else:
        print("zip path not generated")
    
    
#----------------------------------------------------------------------------------------------------- 

     

app.add_api_route("/", oauth.home, methods=["GET"])
app.add_api_route("/spot-login", oauth.spotify_login, methods=["GET"])
app.add_api_route("/callback", oauth.auth_response, methods=["GET"])
app.add_api_route("/playlists", oauth.get_playlists, methods=["GET"])
app.add_api_route("/tracks", oauth.get_tracks, methods=["GET"])
app.add_api_route("/refresh-token", oauth.refresh_token, methods=["GET"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
