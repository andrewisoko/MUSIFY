from dotenv import load_dotenv,find_dotenv
import os
import requests

# TO TEST:
# 1) To run the test, change the main.py modules in relative paths.
# 2) Manually retrieve the access token and add it on the .env from oauth_spotufy.py, the output will appear in the fast api server.
# 3) access token available only for an hour.

def test_correct_scope():
    
    load_dotenv(find_dotenv())
    
    baseapi_url = "https://api.spotify.com/v1/me/playlists"
    pl_read_collaborative_token = os.getenv("PL_READ_COLLABORATIVE_TOKEN")
    
    headers = {"Authorization": f"Bearer {pl_read_collaborative_token}"}
    response = requests.get(baseapi_url,headers=headers)
    
    assert response.json()["total"] == 20 # this is the total amount of playlists.

    # if "a" == "a":
    #     print(response.json())
    #     print(pl_read_collaborative_token)
    #     assert False
     
     
def test_correct_scope2():
    
    load_dotenv(find_dotenv())
    
    baseapi_url = "https://api.spotify.com/v1/me/playlists"
    pl_read_private_token = os.getenv("PL_READ_PRIVATE_TOKEN")
    
    headers = {"Authorization": f"Bearer {pl_read_private_token}"}
    response = requests.get(baseapi_url,headers=headers)
    
    assert response.json()["total"] == 20


def test_wrong_scope():
    
    load_dotenv(find_dotenv())
    
    baseapi_url = "https://api.spotify.com/v1/me/playlists"
    pl_modify_private_token = os.getenv("PL_MODIFY_PRIVATE_TOKEN")
    
    headers = {"Authorization": f"Bearer {pl_modify_private_token}"}
    response = requests.get(baseapi_url,headers=headers)
    
    assert response.json()["total"] == 4 
   

    
def test_wrong_scope2():
    
    load_dotenv(find_dotenv())
    
    baseapi_url = "https://api.spotify.com/v1/me/playlists"
    pl_modify_public_token = os.getenv("PL_MODIFY_PUBLIC_TOKEN")
    
    headers = {"Authorization": f"Bearer {pl_modify_public_token}"}
    response = requests.get(baseapi_url,headers=headers)
    
    assert response.json()["total"] == 4

    
 
    