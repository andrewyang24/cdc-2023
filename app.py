import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Function to retrieve the top 50 tracks released between 2000 and 2010 with all audio features
def get_top_tracks(start_year, end_year, limit=50):
    top_tracks = []

    # Authenticate with the Spotify API to get an access token
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
        # Make the API request
        search_url = "https://api.spotify.com/v1/search"
        search_params = {
            "q": f"year:{year}",
            "type": "track",
            "limit": min(50, limit),
        }
        search_response = requests.get(search_url, headers=headers, params=search_params)
        search_data = search_response.json()

        # Get all available details for the tracks, including all audio features
        track_ids = [track['id'] for track in search_data['tracks']['items']]
        audio_features_url = "https://api.spotify.com/v1/audio-features"
        audio_features_params = {
            "ids": ",".join(track_ids),
        }
        audio_features_response = requests.get(audio_features_url, headers=headers, params=audio_features_params)
        audio_features_data = audio_features_response.json()['audio_features']

        for i, track in enumerate(search_data['tracks']['items']):
            # Combine track and audio feature information
            track_info = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'release_date': track['album']['release_date'],
                'popularity': track['popularity'],
                'id': track['id'],
                **audio_features_data[i]  # Include all audio features
            }
            top_tracks.append(track_info)

    return top_tracks

# Get top 50 tracks released between 2000 and 2010 with all audio features
top_tracks_data = get_top_tracks(2000, 2010)

# Create a DataFrame from the obtained data
df_top_tracks = pd.DataFrame(top_tracks_data)

# Save the DataFrame to a CSV file
df_top_tracks.to_csv('spotify-top-50-tracks-data-with-features.csv', index=False)

# Display the DataFrame
print(df_top_tracks.head())
