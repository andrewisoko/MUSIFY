from oauth_spotify import OAuth_Spotify
import json
import bs4 as beautisoup
import yt_dlp


class YoutubeDownloader():
    
    def retrieve_playlists():
        
        """retrieves playlists from json file generated from webpage link."""
        pass
    
    def playist_dir():
        """Creates a playlist directory in the current working directory."""
        pass
        
    def youtube_soup():
        
        """Passing json data to youtube endpoint to retrieve urls"""
        pass
    
    
    def download_audio_as_mp3(video_url):
         
        """Downloads the audio song from youtube"""
    
        ydl_opts = {
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
                    ydl.download([video_url])

    download_audio_as_mp3('')



