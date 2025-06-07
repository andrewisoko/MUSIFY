from oauth_spotify import OAuth_Spotify
from dotenv import load_dotenv
import json
import requests
import os
import yt_dlp


class YoutubeDownloader():
    
    def retrieve_playlists(self):
        
        """Retrieves spotify playlists from json file generated from webpage link."""
        
        with open("all_tracks.json","r") as read_file:
            self.playlists_json_data = json.load(read_file)
            
        self.trial_playlist = self.playlists_json_data[0] #trial
        
        for key,value in self.trial_playlist.items():
            self.playlist_name = key
            
        
      
        
    def youtube_audio_url(self):
        
        """Passing json artist and song data on youtube endpoint to retrieve song url"""
        
        
        search_url = "https://www.googleapis.com/youtube/v3/search"
        load_dotenv(dotenv_path="src/.env")
    
        for song in self.trial_playlist:
            song = self.trial_playlist[song][0] #trial
            
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
      
        
        
    
    def download_audio_as_mp3(self):
         
        """Downloads the audio song from youtube"""
        
        project_dir = os.path.dirname(os.path.abspath(__file__))
        target_dir = os.path.join(project_dir, '..', f"{self.playlist_name}") 
    
        ydl_opts = {
        
            'paths': {'home': f'{target_dir}'},
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(artist)s - %(title)s.%(ext)s',  
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  
                'preferredquality': '0', 
            }],
            'quiet': False,  
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.yt_audio_endpoint])





youtube_dow = YoutubeDownloader()
youtube_dow.retrieve_playlists()
youtube_dow.youtube_audio_url()

print(youtube_dow.download_audio_as_mp3())