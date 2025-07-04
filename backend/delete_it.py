import os 
import zipfile
import re

class DeleteIt():
    
    def __init__(self): 
        
        self.current_dir = os.path.abspath(__file__)
        self.backend_dir = os.path.dirname(self.current_dir)
        self.musify_dir = os.path.dirname(self.backend_dir)
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self. plst_path_main = os.path.join(self.project_dir,"Playlists downloads")
        self.zip_path_main = os.path.join(self.backend_dir,"zip playlist")
        self.zip_audio_path = os.path.join(self.backend_dir,"Youtube downloads.zip")
        self.playlists_cache = os.path.join(self.backend_dir,"playlists_cache.json")
        self.yt_audio_path =  os.path.join(self.project_dir, "Youtube Downloads","downloads") 
        self.all_tracksjson = os.path.join(self.musify_dir,"frontend", "public","services","allTracks.json")
        
        
    
    def delete_playlistsdirectory(self,name_plst):
        
        """Deletes playlist from backend directory."""
        
        plst_path = os.path.join(self.project_dir,"Playlists downloads",name_plst,"downloads")
        list_audios = os.listdir(plst_path)
        for audio_file in list_audios:
            os.remove(os.path.join(plst_path,audio_file))
        os.rmdir(path=plst_path)
        os.rmdir(os.path.dirname(plst_path))
        os.rmdir(self.plst_path_main)

    
        
        
    def delete_zipplaylist(self,playlist_name:str):
    
        """Deletes zip playlist from backend directory."""
        
        zip_path = os.path.join(self.backend_dir,"zip playlist", f"{playlist_name}.")
        
        if os.path.exists(zip_path):
            
            with open(zip_path, "rb") as file: 
                playlist_zip_file = zipfile.ZipFile(file)
                for items in playlist_zip_file.namelist():
                    filename = os.path.basename(items)
                    if not filename:
                        continue
                    else:
                        source = playlist_zip_file.open(items)
            os.remove(zip_path)
            os.rmdir(self.zip_path_main)
        else:
            print("zip path playlist not generated")

    
    
    def delete_audio_dir(self):
        
        """Deletes yt audio directory from backend directory."""
        
        list_audios = os.listdir(self.yt_audio_path)
        for audio_file in list_audios:
            os.remove(os.path.join(self.yt_audio_path,audio_file))
        os.rmdir(path=self.yt_audio_path)
        os.rmdir(path=os.path.join(self.project_dir, "Youtube Downloads"))
        
        
        
    def delete_audiozip(self):
     
        """Deletes audio zip from backend directory."""
        
        
        if os.path.exists(self.zip_audio_path):
            
            with open(self.zip_audio_path,"rb") as file:
                playlist_zip_file = zipfile.ZipFile(file)
                for items in playlist_zip_file.namelist():
                    filename = os.path.basename(items)
                    if not filename:
                        continue
                    else:
                        source = playlist_zip_file.open(items)
            os.remove(self.zip_audio_path)
        else:
            print("zip path audio not generated")
            
    
    def delete_alltracks_cache(self):

        
        if os.path.exists(self.all_tracksjson):
            os.remove(self.all_tracksjson)

                 
    def delete_playlistsjson_cache(self):
        
        if os.path.exists(self.playlists_cache):
            os.remove(self.playlists_cache)
    
    
    def delete_all(self):
        
        if os.path.exists(self.plst_path_main):
            pl_main_dir = os.listdir(self.plst_path_main)
            for item in pl_main_dir:
                name_plst = item
           
        
        if os.path.exists(self.zip_path_main):
            zip_path_dir = os.listdir(self.zip_path_main)
            for item in zip_path_dir:
                playlist_name = item
      
        for loops in range(6):
        
            if os.path.exists(os.path.join(self.project_dir,"Playlists downloads")):
                self.delete_playlistsdirectory(name_plst=name_plst)
                print("PL Download eliminated")
            elif os.path.exists(os.path.join(self.backend_dir,"zip playlist")):   
                self.delete_zipplaylist(playlist_name=playlist_name) 
                print("Zip playlist eliminated")
            elif os.path.exists(self.yt_audio_path):
                self.delete_audio_dir()
                print("Audio file eliminated")
            elif os.path.exists(self.zip_audio_path):
                self.delete_audiozip()
                print("Audio zip eliminated")
            elif os.path.exists(self.all_tracksjson):
                self.delete_alltracks_cache()
                print("AllTracks json eliminated")
            elif os.path.exists(self.playlists_cache):
                self.delete_playlistsjson_cache()
                print("Playlist json cache eliminated")
                
        return "All generated items deleted."
                
