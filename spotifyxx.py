from base64 import b16decode
import sys 
import numpy
import pandas
import spotipy
import cluster
import spotipy.util as util
from scipy.spatial.distance import cdist



def main():
    username = sys.argv[1]
    scope = 'playlist-modify-private playlist-modify-public user-read-playback-state user-read-currently-playing user-read-private user-read-playback-position user-top-read user-read-recently-played user-library-modify user-library-read user-read-email'
    client_id = '56e103a24afc40559a2ec1ebf71ffd24'
    client_secret = 'e3eb8a5166e2426e99a2a3c376a98dd5'
    redirect_uri = 'https://www.google.com/'



    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

    sp = spotipy.Spotify(auth=token)
    song_data = cluster.song_data

    def get_track_data(track_ids):
        data = []
        for i in range(len(track_ids)):
            a = sp.audio_features(track_ids[i])
            data.append(a[0])
        for i in range(len(track_ids)):
            if data[i] == None:
                continue
            a = sp.track(track_id=track_ids[i])
            data[i]['name'] = a['name']
            data[i]['artists'] = []
            for j in a['artists']:
                data[i]['artists'].append(j['name'])
            data[i]['year'] = int(a['album']['release_date'][:4])
            data[i]['explicit'] = int(a['explicit'])
            data[i]['popularity'] = a['popularity']
            data[i].pop('track_href')
            data[i].pop('analysis_url')
            data[i].pop('uri')
            data[i].pop('type')
            data[i].pop('time_signature')
        return data

    def recommend_tracks(tracks_id):
        track_data = get_track_data(tracks_id)
        song_vectors = []
        headersCSV = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']
        for track in track_data:
            tr = pandas.DataFrame(track)
            song_vector = tr[headersCSV].values
            if song_vector.any() == None:
                continue
            for i in song_vector:
                song_vectors.append(i) 
        song_matrix = numpy.array(list(song_vectors))
        b = numpy.mean(song_matrix, axis=0)

        # Find closest songs to the last played tracks
        scaler = cluster.song_cluster_pipeline.steps[0][1]
        scaled_data = scaler.transform(song_data[headersCSV])
        scaled_b = scaler.transform(b.reshape(1, -1))
        distances = cdist(scaled_b, scaled_data, 'cosine')
        index = list(numpy.argsort(distances)[:, :3][0])

        rec_songs = song_data.iloc[index]
        return rec_songs


    a = sp.current_user_playlists()
    check = 0
    for i in a['items']:
        if i['name'] == "recommendati":
            check = 1
            playlist_id = i['id']
            break

    if check == 0:
        playlist_id = sp.user_playlist_create(user='8acl295jccm62vfl8d90qtvvj', name="recommendati")['id']

    print(playlist_id)

    a = sp.current_user_recently_played(limit=50)
    last_played = []
    for track in a['items']:
        last_played.append(track['track']['id'])

    rec = []
    for i in range(5, 50, 5):
        rec_songs = recommend_tracks(last_played[i-5:i])
        rec.append(rec_songs['id'].values)

    existing_tracks = []
    for i in range(0,1000,50):
        a = sp.playlist_tracks(playlist_id, offset=i)
        for j in range(len(a['items'])):
            existing_tracks.append(a['items'][j]['track']['uri'])

    to_add = []
    print(existing_tracks)
    for i in rec:
        for j in i:
            k = 'spotify:track:' + j
            if k in existing_tracks:
                continue
            to_add.append(k)

    if len(to_add) > 0:
        sp.user_playlist_add_tracks(user='8acl295jccm62vfl8d90qtvvj', playlist_id=playlist_id, tracks=to_add)
    else:
        print("yessss")
        return playlist_id

if __name__ == '__main__':
    main()