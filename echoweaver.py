import json 
from flask import Flask, request, redirect
import requests
import sys
import os
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyOAuth
import webbrowser

app = Flask(__name__)
def run_server():
    app.run(port=8000)

def shutdown_server():
    """Shut down the Flask server gracefully"""
    print( 'Server shutting down...')
    sys.exit("Server shutting down...")

def get_user_credentials(username):
    file_path = os.path.join(os.getcwd(), "access/spotify/secrets.json")
    
    try:
        # Open the file and then load the JSON content
        with open(file_path, 'r') as file:
            secrets_data = json.load(file)  # Parse the JSON data from the file
        return secrets_data
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON file.")
    except IOError:
        print("Error: There was an issue reading the file.")
    try:
        secrets_data[username]
    except KeyError:
        raise Exception("User Credentials Not Found!")
    
class EchoWeaver:
    def __init__(self, username) -> None:
        self.credentials=None
        self.username = username
        self.clientID = None
        self.clientSecret = None
        self.redirect_uri = 'http://127.0.0.1:8000'
        self.spotify_object = None
        self.get_user_credentials()
        self.spotify_access_object = self.create_auth_object()
    
    def get_user_credentials_from_file(self):
        file_path = os.path.join(os.getcwd(), "access/spotify/secrets.json")
        # Reading the secerts file
        try:
            # Open the file and then load the JSON content
            with open(file_path, 'r') as file:
                secrets_data = json.load(file)  # Parse the JSON data from the file
        except FileNotFoundError:
            print(f"Error: The file at {file_path} was not found.")
            raise Exception(f"Error: The file at {file_path} was not found.")
        except json.JSONDecodeError:
            print("Error: The file is not a valid JSON file.")
            raise Exception("Error: The file is not a valid JSON file.")
        except IOError:
            print("Error: There was an issue reading the file.")
            raise Exception("Error: There was an issue reading the file.")
        
        # Fetching User Credentials
        try:
            self.credentials = secrets_data[self.username]
        except KeyError:
            raise Exception("User Credentials Not Found!")
    
    def get_user_credentials(self):
        try:
            self.get_user_credentials_from_file() 
            print(f"Assigned Credentials : {self.credentials}")
            self.clientID = self.credentials['Credentials']['Client ID']
            self.clientSecret = self.credentials['Credentials']['Client Secret']
            self.redirect_uri = 'http://127.0.0.1:8000'
        except Exception as e:
            print(f"Threw Exception {e}")
            raise e
        
    def create_auth_object(self):
        oauth_object = SpotifyOAuth(self.clientID, self.clientSecret, self.redirect_uri, scope=["user-read-playback-state", 
                                                      "user-read-currently-playing", 
                                                      "playlist-read-private"], app_server=app) 
        token_dict = oauth_object.get_access_token() 
        token = token_dict['access_token'] 
        self.spotify_object = Spotify(auth=token, ) 
        return self.spotify_object

    def get_user_queue(self):
        current_track = self.spotify_access_object.current_playback()
        if current_track is not None:
            print("Currently playing:", current_track['item']['name'])
        else:
            print("No track currently playing.")

        # Get current queue (if available)
        queue = []
        queue = self.spotify_access_object.queue()
        print("Current Queue is : \n")
        for song in queue['queue']:
            print(song['name']+"\n")
        # print(queue['queue'][0]['name'])
        
    

username = "LavaHawk01"#input("Enter Username : ")
"""
credentials = get_user_credentials(username=username) 
print(credentials)
username = credentials[username]['username']
clientID = credentials[username]['Credentials']['Client ID']
clientSecret = credentials[username]['Credentials']['Client Secret']
redirect_uri = 'http://127.0.0.1:8000'

print("Starting Authentication")
oauth_object = SpotifyOAuth(clientID, clientSecret, redirect_uri, scope=["user-read-playback-state", 
                                                      "user-read-currently-playing", 
                                                      "playlist-read-private"], app_server=app) 
token_dict = oauth_object.get_access_token() 
token = token_dict['access_token'] 
spotifyObject = Spotify(auth=token, ) 
user_name = spotifyObject.current_user()
"""

app_obj = EchoWeaver(username) 

try:
    while True:
        print("Welcome to the project, " + app_obj.username) 
        print("0 - Exit the console") 
        print("1 - Search for a Song") 
        print("2 - Get Current Playback") 
        user_input = int(input("Enter Your Choice: ")) 
        if user_input == 1: 
            search_song = input("Enter the song name: ") 
            results = app_obj.spotify_access_object.search(search_song, 1, 0, "track") 
            songs_dict = results['tracks'] 
            song_items = songs_dict['items'] 
            song = song_items[0]['external_urls']['spotify'] 
            webbrowser.open(song) 
            print('Song has opened in your browser.') 
        elif user_input == 2:
            app_obj.get_user_queue()
        elif user_input == 0: 
            shutdown_server()
            print("Good Bye, Have a great day!") 
            break
        else: 
            print("Please enter valid user-input.") 

except Exception as e:
    print(f"Threw Exception {str(e)}")
    shutdown_server()