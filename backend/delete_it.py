import os 
import time
import zipfile

class DeleteIt():
    
    def __init__(self):
        
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.yt_audio_path =  os.path.join(self.project_dir, "Youtube Downloads","downloads") 
        self.current_dir = os.path.abspath(__file__)
        self.backend_dir = os.path.dirname(self.current_dir)
        
        
    
    def delete_playlistsdirectory(self,playlist_name):
        
        """Deletes playlist from backend directory."""
        
        plst_path = os.path.join(self.project_dir,"Playlists downloads",playlist_name,"downloads")
        list_audios = os.listdir(plst_path)
        for audio_file in list_audios:
            os.remove(os.path.join(plst_path,audio_file))
        os.rmdir(path=plst_path)
        os.rmdir(os.path.dirname(plst_path))
        os.rmdir(os.path.abspath(self.project_dir,"Playlists downloads"))
        
        
        
    def delete_zipplaylist(self,playlist_name:str):
    
        """Deletes zip playlist from backend directory."""
        
        zip_path = os.path.join(self.backend_dir,f"{playlist_name}.zip")
        
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
        else:
            print("zip path not generated")
    
    
    
    def delete_yt_download_dir(self):
        
        """Deletes yt audio directory from backend directory."""
        
        list_audios = os.listdir(self.yt_audio_path)
        for audio_file in list_audios:
            os.remove(os.path.join(self.yt_audio_path,audio_file))
        os.rmdir(path=self.yt_audio_path)
        os.rmdir(path=os.path.join(self.project_dir, "Youtube Downloads"))
        
        
        
    def delete_audiozip(self):
     
        """Deletes audio zip from backend directory."""
        
        zip_audio_path = os.path.join(self.backend_dir,"Youtube downloads.zip")
        
        if os.path.exists(zip_audio_path):
            
            with open(zip_audio_path, "rb") as file:
                playlist_zip_file = zipfile.ZipFile(file)
                for items in playlist_zip_file.namelist():
                    filename = os.path.basename(items)
                    if not filename:
                        continue
                    else:
                        source = playlist_zip_file.open(items)
            os.remove(zip_audio_path)
        else:
            print("zip path not generated")
    

    

