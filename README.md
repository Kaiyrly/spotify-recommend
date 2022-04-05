# spotify-recommend
Spotify recommendation system: An app which creates a new playlist with recommendations based on User’s recently listened tracks. It is developed by Python, using Spotify Web API. 
Process consisted of 2 parts: data collection, data analysis and music recommendation.

Data collection - At first I downloaded a dataset from internet, then completed it using Spotify Web API. Dataset contains around 650000 tracks. It consists of track name, artists, release date, genre and different features such as loudness, danceability, temp etc.
	
Music recommendation - app takes recently played tracks using Spotify Web API. Then, makes a matrix of tracks containing track data. Then computes mean vector of the audio data and features for these tracks. After this, app uses cosine distance to find the n closest songs to the mean vector. Finally, makes a playlist with these songs.
