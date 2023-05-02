from base64 import b16decode
import sys
import numpy as np
import pandas as pd
import spotipy
import spotipy.util as util
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Configuration
username = "8acl295jccm62vfl8d90qtvvj"
scope = 'playlist-modify-private playlist-modify-public user-read-playback-state user-read-currently-playing user-read-private user-read-playback-position user-top-read user-read-recently-played user-library-modify user-library-read user-read-email'
client_id = '56e103a24afc40559a2ec1ebf71ffd24'
client_secret = 'e3eb8a5166e2426e99a2a3c376a98dd5'
redirect_uri = 'https://www.google.com/'

# Get Token
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

sp = spotipy.Spotify(auth=token)
song_data = pd.read_csv('data/data.csv')

# Filter the necessary headers
headersCSV = ['valence', 'year', 'acousticness', 'artists', 'danceability', 'duration_ms', 'energy', 'explicit', 'id', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'name', 'popularity', 'release_date', 'speechiness', 'tempo']
song_data = song_data[headersCSV]

song_cluster_pipeline = Pipeline([('scaler', StandardScaler()),
                                  ('kmeans', KMeans(n_clusters=20,
                                                    verbose=2))], verbose=True)

X = song_data.select_dtypes(np.number)
song_cluster_pipeline.fit(X)
song_cluster_labels = song_cluster_pipeline.predict(X)
song_data['cluster_label'] = song_cluster_labels
