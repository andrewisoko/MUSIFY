
 <div align="center">

 # MUSIFY🎵

</div>

## Getting started

In order to successfully run the program you need to add:

1) Id and secret client, from the spotify developer webpage. https://developer.spotify.com/documentation/web-api/concepts/apps 

   - Then add them on the .env file
     
  - A personal session key on this section of the code in main.py:

```

app.add_middleware(
    SessionMiddleware,
    secret_key= "add key"
)
```

2) Go to the backend directory from the terminal

```
cd ./backend/
```

 Activate the musifyvenv virtual environment.

```
musifyvenv/Scripts/Activate
```
install the requirements.txt:

```
pip install -r requirements.txt
```

To run the fast api server:

```
python main.py 
```

3) Open a second terminal and go to frontend directory

```
cd ./frontend/
```

run:

```
npm run dev
```

Click the local enpoint from the terminal (Local:   http://127.0.0.1:5173/)

## tests

1) To run tests it is required to activate the virtual environment then:
   
```
cd ./backend/
```

3) To run test:

```
python -m pytest
```

4) Running the test_playlists.py will result in an  "assert response.json()["total"] == 20" error.
To test the test_playlists.py add the access token to the .env file, unfortunately it is a manual process so it is required to

* run the backend server 
* print the access token 
* copy the result from the backend server and paste it to the .env file 

## Project structure


![ image alt](https://github.com/andrewisoko/MUSIFY/blob/main/images/musify%20diagram.png)

1) The frontpage will initially display two options for the user:
   - Login to spotify
   - Download an audio.
 2) When running the backend all the playlist files,zip files and cache data from previous session get deleted with a function:
```
if __name__ == "__main__":
    
    print(cleanup.delete_all()) #deletes previous items created.
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
```
3) If the spotify button gets clicked:
   
   - It will send an api request at the /spot-login endpoint.
   - Auth process for the spotify auth url redirect page.
   - Backend code provided from the auth process will be exchanged for tokens.
   - Then api request at /playlists and /tracks endpoint to grant access to spotify playlists data.
   - Generates of a playlist cache file and alltracks json file in the backend.
   - Frontend renders the page with the playlists data.
   - 
5) When clicking the download button of a playlist:
   
   - It will send an api request at the /download-playlist endpoint.
   -  A playlist folder gets created in the backend directory.
   - These two functions generate the playlist folders:
     
     ```
         def download_audio_as_mp3(self) -> str:
         
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
               
                    

       def download_selected_playlist(self,playlist_name) -> str:
           
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

     
      - Folder icon appears in the webpage, playlist card. Only available temporarily.
      - Api request at the /delete-playlist endpoint.
      - Playlist folder deleted from the backend directory.

 6) If folder icon clicked.

    - Api request at /zipplaylist-download endpoint.
    - It generates a zipfile of the playlist in the backend.
    - The folder icon will contain the zip playlist link. Only available temporarily.
    - Then api request at /zipdelete-playlist endpoint.
    - Zipfile deleted from the backend directory.
   
7) For The audio download the process is almost identical with the only difference in endpoints, and no interaction with spotify.

## What's next

1) Buliding a sign up page.
2) Set a database.
3) Restriction to playlist downloads.

## Contact me

If you have any questions about the project, please feel free to contact me on https://www.linkedin.com/in/andrew-isoko/ I’ll be glad to assist you.

