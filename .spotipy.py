import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
import pandas as pd
from dotenv import load_dotenv
import os
import time

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Authenticate with the Spotify API
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Function to retrieve the top 100 tracks released between 2000 and 2010
def get_tracks(start_year, end_year, limit=50):
    tracks = []

    for year in range(start_year, end_year + 1):
        # Search for tracks released in a specific year
        results = sp.search(q=f'year:{year}', type='track', limit=min(50, limit))

        # Get all available details for the tracks, including all audio features
        track_ids = [track['id'] for track in results['tracks']['items']]
        audio_features = sp.audio_features(track_ids)

        for i, track in enumerate(results['tracks']['items']):
            # Combine track and audio feature information
            track_info = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'release_date': track['album']['release_date'],
                'popularity': track['popularity'],
                'id': track['id'],
                **audio_features[i]  # Include all audio features
            }
            tracks.append(track_info)

    return tracks


# Get top 100 tracks released between 2000 and 2010
top_tracks_data = get_tracks(2000, 2010)

# Create a DataFrame from the obtained data
df_top_tracks = pd.DataFrame(top_tracks_data)

# Save the DataFrame to a CSV file
df_top_tracks.to_csv('spotify-top-tracks-data.csv', index=False)

# Display the DataFrame
print(df_top_tracks.head())
