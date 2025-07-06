import os
import tempfile
import zipfile
import pytest

from backend.delete_it import DeleteIt  

@pytest.fixture
def fake_filesystem():
    with tempfile.TemporaryDirectory() as tempdir:
        
        """Creating an emulation directory with all the necesary file paths."""
        
        musify_dir = os.path.join(tempdir, "musify")
        backend_dir = os.path.join(tempdir, "backend")
        frontend_dir = os.path.join(musify_dir, "frontend", "public", "services")
        
        plst_downloads = os.path.join(tempdir, "Playlists downloads", "playlist1", "downloads")
        zip_playlist_dir = os.path.join(backend_dir, "zip playlist")
        zip_file_path = os.path.join(zip_playlist_dir, "dummy.zip")
        yt_downloads = os.path.join(tempdir, "Youtube Downloads", "downloads")
        zip_audio_path = os.path.join(backend_dir, "Youtube downloads.zip")
        playlists_cache = os.path.join(backend_dir, "playlists_cache.json")
        all_tracksjson = os.path.join(frontend_dir, "allTracks.json")
        

        os.makedirs(plst_downloads)
        with open(os.path.join(plst_downloads, "song.mp3"), "w") as f:
            f.write("dummy audio")
        
      
        os.makedirs(backend_dir, exist_ok=True)
        os.makedirs(frontend_dir, exist_ok=True)
        os.makedirs(zip_playlist_dir, exist_ok=True)
        os.makedirs(yt_downloads)
        
        
        
        with open(os.path.join(yt_downloads, "yt_song.mp3"), "w") as f:
            f.write("dummy yt audio")
            
        with zipfile.ZipFile(zip_file_path,"w") as myzip:
            myzip.writestr(data= "dummy.txt",zinfo_or_arcname="dummy.zip")

        with zipfile.ZipFile (zip_audio_path,"w") as audiozip:
            audiozip.writestr(data="audio dummy.txt", zinfo_or_arcname = "Youtube downloads.zip")
        with open(all_tracksjson, "w") as f:
            f.write("{}")
 
        with open(playlists_cache, "w") as f:
            f.write("{}")
        
        yield tempdir  


def test_delete_all(fake_filesystem):

    cleanup_test = DeleteIt()

    if os.path.exists(os.path.join(
        fake_filesystem, "Playlists downloads", "playlist1", "downloads")
        ) and os.path.exists(os.path.join(
        fake_filesystem,"backend", "zip playlist")
        ) and os.path.exists(os.path.join(
        fake_filesystem,"backend", "Youtube downloads.zip")
        ) and os.path.exists(os.path.join(
        fake_filesystem, "Youtube Downloads","downloads")
        ) and os.path.exists(os.path.join(
        fake_filesystem,"backend","playlists_cache.json")
        ) and os.path.exists(os.path.join(
        fake_filesystem,"musify","frontend", "public", "services","allTracks.json")):
            
        print(cleanup_test.delete_all())
        assert True
        
    else:
        assert False
        

            
    
   


  
    