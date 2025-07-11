import json
import os
import yt_dlp
from yt_dlp import YoutubeDL
from pytube import extract
from yt_dlp.utils import DownloadError
import time



class YoutubeDownloader():
    
    
    def __init__(self):
        
        self.playlists_json_data = None
        self.json_all_playlists = None
        self.playlist_name = None
        self.playlist_allsongs = None
        self.yt_audio_url = None
        self.videoId_url_list = None
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.parent_directory = os.path.dirname(self.project_dir)
     
       
             
    
    def retrieve_playlists(self):
        
        """Reads all_tracks.json file."""
        
        
        load_path = os.path.join(self.parent_directory,"frontend","public","services")
        
        with open(f"{load_path}/allTracks.json","r") as read_file:
            self.playlists_json_data = json.load(read_file)
            

    
    def youtube_audio_url(self) -> list: 
        
        """Returns a list of youtube video urls ex:(https://www.youtube.com/watch?v=wLsWOxrB7N9)""" 
        
        self.videoId_url_list = []
        
        index_track = 0

        while len(self.playlist_allsongs) > index_track:
            song = self.playlist_allsongs[index_track]
                        
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                try:
                    result = ydl.extract_info(f"ytsearch1:{song}", download=False)
                    video = result['entries'][0]
                    self.yt_audio_url = (video['webpage_url']) 
                    video_id = extract.video_id(self.yt_audio_url)
                    share_yt_url = f"https://youtu.be/{video_id}"
                except Exception as err:
                    print(f"problem with {share_yt_url}, {err}")
                self.videoId_url_list.append({self.playlist_allsongs[0]:share_yt_url})
            index_track += 1
                    
        return self.videoId_url_list           
         
         
        
    def download_audio_as_mp3(self):
         
        """Downloads the audio song from the url youtube list."""
        
        download_target_dir = os.path.join("Playlists downloads",self.playlist_name)
        ffmpeg_bin = os.path.abspath(os.path.join(self.project_dir, '.', 'ffmpeg', 'bin'))
        
    
        ydl_opts = {
        
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(artist)s - %(title)s.%(ext)s',  
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  
                'preferredquality': '320', 
            }],
            'quiet': False,  
            'paths': {'home': f'{download_target_dir}'},
             'ffmpeg_location': ffmpeg_bin,
            'socket_timeout': 2,   
            'force_ipv4': True,
        }
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for audios in range((len(self.videoId_url_list))):
                dict_url = self.videoId_url_list[0]
                for title_key, url in dict_url.items():
                    audio_url = url
                    
                audio_name_songtitle = self.playlist_allsongs[0]
                ydl.download([audio_url])
                
                print(f"{audio_name_songtitle} MP3 file downloaded.")
                
                self.videoId_url_list.pop(0)
                self.playlist_allsongs.pop(0)
                    
                    

    def download_selected_playlist(self,playlist_name):
        
        """Downloads spotify playlist based on user choice."""
        
        playlist_name_list = [plst_name for dictionaries in self.playlists_json_data for plst_name,values in dictionaries.items()]
       
        if playlist_name in playlist_name_list:
            index = playlist_name_list.index(playlist_name)
            
            playlist_selected = self.playlists_json_data[index]
        
            for key,value in playlist_selected.items():
                self.playlist_name = key
                self.playlist_allsongs = value
                
                self.youtube_audio_url()
                self.download_audio_as_mp3()
            
                 
            
    def download_from_yt_link(self,audio_url) -> str:
        
        """Downloads audio direclty from youtube."""
        
        
        download_target_dir = os.path.join(self.project_dir, "Youtube Downloads") 
        ffmpeg_bin = os.path.abspath(os.path.join(self.project_dir, '.', 'ffmpeg', 'bin'))
        
    
        ydl_opts = {
        
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(artist)s - %(title)s.%(ext)s',  
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  
                'preferredquality': '320', 
            }],
            'quiet': False,  
            'paths': {'home': f'{download_target_dir}'},
             'ffmpeg_location': ffmpeg_bin,
            'socket_timeout': 2,   
            'force_ipv4': True,
        }
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
              ydl.download([audio_url])
              return "Audio downloaded"
          
            except DownloadError as err:
                print(f"audio not found: {err}")
         

        
       