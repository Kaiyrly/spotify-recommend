from flask import Flask, request, jsonify, render_template
import cluster
import spotifyxx
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    username = request.form['username']
    sys.argv = ['', username]  # Temporarily set sys.argv for the existing code to work

    try:
        playlist_id = spotifyxx.main()
        return jsonify({'playlist_id': playlist_id})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
