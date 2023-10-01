import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# load environment variables to get client id and secret
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_top_tracks(start_year, end_year, limit=50):
    top_tracks = []

    # Authenticate with the Spotify API to get an access token (chatgpt)
    auth_url = "https://accounts.spotify.com/api/token"
    auth_data = {
        "grant_type": "client_credentials",
    }
    auth_response = requests.post(auth_url, auth=(client_id, client_secret), data=auth_data)
    access_token = auth_response.json().get("access_token")

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    for year in range(start_year, end_year + 1):
        search_url = "https://api.spotify.com/v1/search"
        search_params = {
            "q": f"year:{year}",
            "type": "track",
            "limit": min(50, limit),
        }
        search_response = requests.get(search_url, headers=headers, params=search_params)
        search_data = search_response.json()

        for track in search_data['tracks']['items']:
            # Get artist details to retrieve genres
            artist_id = track['artists'][0]['id']
            artist_url = f"https://api.spotify.com/v1/artists/{artist_id}"
            artist_response = requests.get(artist_url, headers=headers)
            artist_data = artist_response.json()

            # Get all available details for the tracks, including all audio features
            audio_features_url = "https://api.spotify.com/v1/audio-features"
            audio_features_params = {
                "ids": track['id'],
            }
            audio_features_response = requests.get(audio_features_url, headers=headers, params=audio_features_params)
            audio_features_data = audio_features_response.json()['audio_features'][0]

            # Compile track info
            track_info = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'release_date': track['album']['release_date'],
                'popularity': track['popularity'],
                'id': track['id'],
                'genres': artist_data.get('genres', []),
                **audio_features_data
            }
            top_tracks.append(track_info)

    return top_tracks

# Save to df and csv
top_tracks_data = get_top_tracks(2000, 2010)
df_top_tracks = pd.DataFrame(top_tracks_data)
df_top_tracks.to_csv('./data/spotify-data.csv', index=False)
print(df_top_tracks.head())