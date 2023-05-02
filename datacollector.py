import sys
import spotipy
from csv import DictWriter
import spotipy.util as util

# Configuration
username = sys.argv[1]
scope = 'playlist-modify-private playlist-modify-public user-read-playback-state user-read-currently-playing user-read-private user-read-playback-position user-top-read user-read-recently-played user-library-modify user-library-read user-follow-modify ugc-image-upload'
client_id = '124ca109d7d5402b8ce9a4cbe366326b'
client_secret = '27c3f19ade7a49c286613f1c8e4002d3'
redirect_uri = 'https://www.google.com/'

# Get Token
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

sp = spotipy.Spotify(auth=token)


# Get audio features using the track id
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


# Collect all artist id, existing in the playlists
def collect_artist_ids(playlist_id):
    artist_ids = []
    
    for i in range(0,1000,50):
        a = sp.playlist_tracks(playlist_id, offset=i)
        
        for k in range(len(a['items'])):
            # print(a['items'][i]['track']['album']['artists'])
            # print('---------------------------')
            for j in a['items'][k]['track']['album']['artists']:
                f = open('data/artists.txt', 'r')
                Lines = f.readlines()
                f.close()
                if j['id'] + '\n' in Lines:
                    print('Already in the list')
                    continue
                f = open("data/artists.txt", "a")
                f.write("{}\n".format(j['id']))
                f.close()


# Collect artists all tracks
def collect_artist_data(artist_id):
    track_ids = []
    tracks = []
    for i in range(0,100,50):
        a = sp.artist_albums(artist_id, offset=i)
        print("=+=+=+=+=+=+=+=+=+=+")
        for j in range(len(a['items'])):
            if a['items'][j]['album_type'] == 'single':
                c = {}
                # c['release_date'] = a['items'][j]['release_date']
                c['artists'] = a['items'][j]['artists']
                c['name'] = a['items'][j]['name']
                if c in tracks:
                    print('ooooooooooo')
                    continue  
                tracks.append(c)
                track_ids.append(a['items'][j]['id'])
                print(a['items'][j]['name'])
            else:
                b = sp.album_tracks(a['items'][j]['id'])
                for k in range(len(b['items'])):
                    c = {}
                    # print(b['items'][k])
                    c['artists'] = b['items'][k]['artists']
                    c['name'] = b['items'][k]['name']
                    if c in tracks:
                        print('ffffffffffffff')
                        continue  
                    tracks.append(c)
                    track_ids.append(b['items'][k]['id'])
                    print(b['items'][k]['name'])
    return get_track_data(track_ids)

# a = sp.current_user_playlists()
# artist_ids = []
# check = {}
# for i in a['items']:
#     collect_artist_ids(i['id'])
a = sp.current_user_recently_played(limit=50)
print(a)
f = open('data/artists.txt', 'r')
Lines = f.readlines()
f.close()
headersCSV = ['valence', 'year', 'acousticness', 'artists', 'danceability', 'duration_ms', 'energy', 'explicit', 'id', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'name', 'popularity', 'release_date', 'speechiness', 'tempo']
for i in Lines:
    # check if we already have artist's tracks
    f = open('data/saved_artists.txt', 'r')
    lines = f.readlines()
    f.close()
    if i in lines:
        print('Already in the list')
        continue
    # if we don't have artist's tracks, collect them
    data = collect_artist_data(i.replace('\n', ''))
    with open('CSVFILE.csv', 'a', newline='') as f_object:  
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        for j in data:
            if j == None:
                continue
            dictwriter_object.writerow(j)
            print(j['name'])
        f_object.close()

    # add artist to the file
    f = open("data/saved_artists.txt", "a")
    f.write(i)
    f.close()