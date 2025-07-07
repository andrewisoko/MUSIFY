import os
import tempfile
import zipfile
import pytest
from pathlib import Path

from backend.delete_it import DeleteIt  

@pytest.fixture
def fake_filesystem():
    with tempfile.TemporaryDirectory() as tempdir:
        
        """Creating an emulation directory with all the necesary file paths."""

        
        plst_downloads = os.path.join(tempdir, "Playlists downloads", "playlist1", "downloads")
        zip_playlist_dir = os.path.join(tempdir, "zip playlist")
        zip_file_path = os.path.join(tempdir,"zip playlist","dummy.zip")
        yt_downloads = os.path.join(tempdir, "Youtube Downloads", "downloads")
        zip_audio_path = os.path.join(tempdir, "Youtube downloads.zip")
        playlists_cache = os.path.join(tempdir, "playlists_cache.json")
        all_tracksjson = os.path.join(tempdir, "frontend", "public", "services","allTracks.json")
        

      
        # os.makedirs(frontend_dir, exist_ok=True)
        os.makedirs(plst_downloads)
        os.makedirs(zip_playlist_dir, exist_ok=True)
        os.makedirs(yt_downloads)
        
        
        with open(os.path.join(plst_downloads, "song.mp3"), "w") as f:
            f.write("dummy audio")
        
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





    
def test_delete_all(monkeypatch, fake_filesystem):
   
    dummy_file = os.path.join(fake_filesystem, "dummy_script.py") #dummy_script.py is the equivalent of __file__ on the os.path.abspath function
    with open(dummy_file, "w") as f:
        f.write("dummy")
    monkeypatch.setattr("os.path.abspath", lambda x =None: dummy_file) # this will result as os.path.abspath(__file__) in the delete_it module
    
    dummy_file_path = (os.path.dirname(dummy_file))
    temp_path = Path(dummy_file_path).resolve().parent
    
 
    deleter = DeleteIt()
    result = deleter.delete_all()
    assert result == "All generated items deleted."

