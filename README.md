
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

1) To run tests it is required to add:

"backend." on every module imported from the backend 

![Alt text](https://github.com/andrewisoko/MUSIFY/blob/main/images/Screenshot%202025-07-05%20110902.png?raw=true)

2) Go to the tests directory from the terminal:

```
cd ./backend/
```

```
cd ./tests/
```

3) To run test:

```
pytest
```

4) Running the test_playlists.py will result in an  "assert response.json()["total"] == 20" error.
To test the test_playlists.py add the access token to the .env file, unfortunately it is a manual process so it is required to

* run the backend server 
* print the access token 
* copy the result from the backend server and paste it to the .env file 

## Project structure

## Contact me

If you have any questions about the project, please feel free to contact me on https://www.linkedin.com/in/andrew-isoko/ I’ll be glad to assist you.

