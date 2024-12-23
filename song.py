from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/get_song', methods=['POST'])
def get_song():
    data = request.json
    song_name = data.get('song_name')
    
    if not song_name:
        return jsonify({"error": "Song name not provided"}), 400

    # Search and extract audio URL
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'default_search': 'ytsearch1'  # Search YouTube and return the first result
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(song_name, download=False)
            audio_url = result['entries'][0]['url'] if 'entries' in result else result['url']
        return jsonify({"audio_url": audio_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
