from oauth_spotify import OAuth_Spotify
from dotenv import load_dotenv
import json
import requests
import os
import yt_dlp
from yt_dlp.utils import DownloadError


class YoutubeDownloader():
    
    def __init__(self):
        
        self.playlists_json_data = None
        self.trial_playlist = None
        self.playlist_name = None
        self.playlist_allsongs = None
        self.yt_audio_endpoint = None
        self.videoId_url_list = None
        
    
    def retrieve_playlists(self):
        
        """Retrieves spotify playlists from json file generated from webpage link."""
        
        with open("all_tracks.json","r") as read_file:
            self.playlists_json_data = json.load(read_file)
            
        self.trial_playlist = self.playlists_json_data[0] #trial
        
        for key,value in self.trial_playlist.items():
            self.playlist_name = key
            self.playlist_allsongs = value
            
        
      
        
    def youtube_audio_url(self):
        
        """Returns a list of youtube video urls ex:(https://www.youtube.com/watch?v=wLsWOxrB7N9)"""
           
        
        search_url = "https://www.googleapis.com/youtube/v3/search"
        load_dotenv(dotenv_path="src/.env")
        self.videoId_url_list = []
    
        for tracks in range(len(self.playlist_allsongs)):
            song = self.playlist_allsongs[0]
            
            params = {
                    "part": "snippet",
                    "q": f"{song}(Audio)",
                    "maxResults": 5,
                    "key": os.getenv("YT_API_KEY")
                }
            
            response = requests.get(search_url, params=params)
            youtube_topfive_response = response.json()
            videoId = youtube_topfive_response["items"][0]["id"]["videoId"]
            
            
            self.yt_audio_endpoint = f'https://www.youtube.com/watch?v={videoId}'
             
            self.videoId_url_list.append({self.playlist_allsongs[0]:self.yt_audio_endpoint})
            self.playlist_allsongs.pop(0)
            
            
        return self.videoId_url_list
        
        
    
    def download_audio_as_mp3(self):
         
        """Downloads the audio song from the url youtube list."""
        
        project_dir = os.path.dirname(os.path.abspath(__file__))
        download_target_dir = os.path.join(project_dir, '..', f"{self.playlist_name}") 
        ffmpeg_bin = os.path.abspath(os.path.join(project_dir, '.', 'ffmpeg', 'bin'))
        
    
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
        }
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for audios in range((len(self.videoId_url_list))):
                audio_url = self.videoId_url_list[0]
                audio_name_songtitle = self.playlist_allsongs[0]
                try:
                    ydl.download([audio_url])
                    self.videoId_url_list.pop(0)
                    self.playlist_allsongs.pop(0)
                    
                    print(f"{audio_name_songtitle} MP3 file downloaded.")
                    
                except DownloadError as err:
                    print(f"{audio_name_songtitle} WEBM file downloaded.\nPlease check {err}")
                    self.videoId_url_list.pop(0)
                    self.playlist_allsongs.pop(0)
                        





youtube_dow = YoutubeDownloader()
youtube_dow.retrieve_playlists()
youtube_dow.youtube_audio_url()
print(youtube_dow.download_audio_as_mp3())