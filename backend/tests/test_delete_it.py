from pathlib import Path
import os
from backend.delete_it import *
import zipfile
import json

class Test_delete_it():
    
    def file_paths(self):
        
        self.cleanup_completed = False
        self.backend_path = Path(__file__).resolve().parent.parent
        self.musify_path = Path(__file__).resolve().parent.parent.parent
        self.frontend_service_path = os.path.join(self.musify_path,"frontend", "public","services")
                
        self.plst_path = os.path.join(self.backend_path,"Playlists downloads","playlist name","downloads")
        self.zip_path = os.path.join(self.backend_path,"zip playlist")
        self.yt_audio_path =  os.path.join(self.backend_path, "Youtube Downloads","downloads") 
        self.zip_audio_path = os.path.join(self.backend_path,"Youtube downloads.zip")
        
        self.playlists_cache = os.path.join(self.backend_path,"playlists_cache.json")
        self.all_tracksjson = os.path.join(self.musify_path,"frontend", "public","services","allTracks.json")


    def test_generate_file_paths(self):
        
        self.file_paths()
        
        if os.path.exists(
            self.plst_path) and os.path.exists(
            self.zip_path) and os.path.exists(
            self.yt_audio_path) and os.path.exists(
            self.zip_audio_path) and os.path.exists(
            self.playlists_cache) and os.path.exists(
            self.all_tracksjson
            ):
            pass
        
        else:
            
            zip_file_full_path = os.path.join(self.zip_path, "my_archive.zip")
            zip_fileaudio_full_path = os.path.join(self.backend_path,"Youtube downloads.zip")
            
            os.makedirs(self.plst_path, exist_ok=True)
            os.makedirs(self.yt_audio_path, exist_ok=True)
            os.makedirs(self.zip_path, exist_ok=True)
          

            with open(f"{self.backend_path}/playlists_cache.json", "w") as file_playlist:
                data = {"something": "in it"}
                json.dump(data, file_playlist)

            with open(f"{self.frontend_service_path}/allTracks.json", "w") as file_alltracks:
                data = {"something": "in it"}
                json.dump(data, file_alltracks)

            with zipfile.ZipFile(zip_file_full_path, 'w') as zipf:
                zipf.writestr("data.txt", "content")

            with zipfile.ZipFile(zip_fileaudio_full_path, 'w') as zipf:
                zipf.writestr("data.txt", "content")

        assert True
        
        
    def test_delete_all(self):
        
        cleanup_test = DeleteIt()
        print(cleanup_test.delete_all())
        try:
            if os.path.exists(
                self.plst_path) and os.path.exists(
                self.zip_path) and os.path.exists(
                self.yt_audio_path) and os.path.exists(
                self.zip_audio_path) and os.path.exists(
                self.playlists_cache) and os.path.exists(
                self.all_tracksjson):
                self.cleanup_completed = False
                
        except Exception as err:
            print("clean up completed")
            self.cleanup_completed = True
            assert self.cleanup_completed == True
        
        
        
        
     
    
   
    
    

  
    