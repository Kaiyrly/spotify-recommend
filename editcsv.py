import pandas
from csv import DictWriter

song_data = pandas.read_csv('tracks2.csv')
headersCSV = ['valence', 'year', 'acousticness', 'artists', 'danceability', 'duration_ms', 'energy', 'explicit', 'id', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'name', 'popularity', 'release_date', 'speechiness', 'tempo']
firstRow = {'valence': 'valence', 'year': 'year', 'acousticness': 'acousticness', 'artists': 'artists', 'danceability': 'danceability', 'duration_ms': 'duration_ms', 'energy': 'energy', 'explicit': 'explicit', 'id': 'id', 'instrumentalness': 'instrumentalness', 'key': 'key', 'liveness': 'liveness', 'loudness': 'loudness', 'mode': 'mode', 'name': 'name', 'popularity': 'popularity', 'release_date': 'release_date', 'speechiness': 'speechiness', 'tempo': 'tempo'}
data = []
for i in song_data:
    for j in range(len(song_data[i])):
        if len(data) <= j:
            x = {}
            data.append(x)
        data[j][i] = song_data[i][j]
    print(i)


# for i in data:
#     print(i)
# with open('CSVFILE.csv', 'a', newline='') as f_object:  
#     dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
#     dictwriter_object.writerow(firstRow)
#     f_object.close()
with open('CSVFILE.csv', 'a', newline='') as f_object:  
    dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
    cnt = 0
    for j in data:
        if j == None:
            continue
        dictwriter_object.writerow(j)
        cnt+=1
        if cnt % 1000 == 0:
            print(cnt)
        # print(j['name'])
    f_object.close()