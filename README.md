# Spotify Recommendation System

Introducing the **Spotify Recommendation System**, a seamless app that curates personalized playlists based on your recently listened tracks. Developed with Python and utilizing the powerful Spotify Web API, this app ensures that you always have a fresh and unique listening experience.

## How It Works

The Spotify Recommendation System consists of two main components: Data Collection and Music Recommendation.

### Data Collection

The foundation of this app is an extensive dataset sourced from the internet, containing information on approximately 650,000 tracks. The dataset is further enriched using the Spotify Web API, providing track names, artists, release dates, genres, and a range of features such as loudness, danceability, and tempo.

### Music Recommendation

The app works its magic by following these steps:

1. Retrieves your recently played tracks using the Spotify Web API.
2. Generates a matrix of track data, including various audio features.
3. Computes a mean vector for the audio data and features of your recently played tracks.
4. Employs cosine distance to determine the 'n' closest songs to the mean vector.
5. Crafts a brand new playlist with these carefully selected tracks.

## Experience the Magic

By integrating the Spotify Recommendation System into your listening routine, you'll discover an innovative way to explore new music tailored to your unique tastes. Say goodbye to the mundane and hello to a world of personalized playlists at your fingertips.
