from flask import Flask, render_template, request, jsonify, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files')
def list_files():
    try:
        downloads_dir = 'downloads'
        if not os.path.exists(downloads_dir):
            return jsonify({'files': []})
        
        files = []
        for filename in os.listdir(downloads_dir):
            if os.path.isfile(os.path.join(downloads_dir, filename)):
                files.append(filename)
        
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/files/<filename>')
def download_file(filename):
    return send_from_directory('downloads', filename)

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.json['url']
        
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'best[height<=480]/worst'
        }
        
        os.makedirs('downloads', exist_ok=True)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return jsonify({'status': 'success', 'message': 'Video downloaded successfully!'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)