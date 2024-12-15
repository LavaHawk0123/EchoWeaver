import requests
import base64

# Replace these with your Spotify credentials
CLIENT_ID = "6f8340d1e58e4e5da8668cf81ff8369d"
CLIENT_SECRET = "811b460723ce40b7b0c4109fc82797ad"
REDIRECT_URI = "http://localhost:8000/callback"

# Step 1: Get the authorization URL
def get_authorization_url():
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "playlist-read-private playlist-modify-private playlist-modify-public",
    }
    return f"{auth_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

# Step 2: Exchange authorization code for access token
def get_access_token(auth_code):
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    base64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {base64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.post(token_url, data=data, headers=headers)
    if response.status_code != 200:
        print("Error in Authorization:", response.json())
    response.raise_for_status()
    return response.json()

# Step 3: Fetch playlist tracks
def get_playlist_tracks(access_token, playlist_id):
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(playlist_url, headers=headers)
    response.raise_for_status()
    tracks = response.json()["items"]
    return [track["track"]["uri"] for track in tracks]

# Step 4: Create a new playlist
def create_playlist(access_token, user_id, name, description="", public=False):
    create_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "name": name,
        "description": description,
        "public": public,
    }
    response = requests.post(create_url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["id"]

# Step 5: Add tracks to the playlist
def add_tracks_to_playlist(access_token, playlist_id, track_uris):
    add_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"uris": track_uris}
    response = requests.post(add_url, json=data, headers=headers)
    response.raise_for_status()

if __name__ == "__main__":
    print("Go to the following URL to authorize:")
    print(get_authorization_url())

    # After user authorizes, they will be redirected with a code
    auth_code = input("Enter the authorization code from the redirect URL: ")
    tokens = get_access_token(auth_code)
    access_token = tokens["access_token"]

    # Get the source playlist ID and user ID
    playlist_id = input("Enter the source playlist ID: ")
    user_id = input("Enter your Spotify user ID: ")

    # Fetch tracks from the source playlist
    print("Fetching tracks from the source playlist...")
    track_uris = get_playlist_tracks(access_token, playlist_id)

    # Create a new playlist
    new_playlist_name = input("Enter a name for the new playlist: ")
    print("Creating the new playlist...")
    new_playlist_id = create_playlist(access_token, user_id, new_playlist_name)

    # Add tracks to the new playlist
    print("Adding tracks to the new playlist...")
    add_tracks_to_playlist(access_token, new_playlist_id, track_uris)

    print(f"New playlist '{new_playlist_name}' created successfully!")
