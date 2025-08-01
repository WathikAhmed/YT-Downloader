from flask import Flask, render_template, request, jsonify, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files')
@app.route('/files/<path:subpath>')
def list_files(subpath=''):
    try:
        downloads_dir = os.path.join('downloads', subpath) if subpath else 'downloads'
        if not os.path.exists(downloads_dir):
            return jsonify({'items': []})
        
        items = []
        for item in os.listdir(downloads_dir):
            if item.startswith('.'):  # Skip hidden files like .DS_Store
                continue
            item_path = os.path.join(downloads_dir, item)
            if os.path.isfile(item_path):
                items.append({'name': item, 'type': 'file'})
            elif os.path.isdir(item_path):
                items.append({'name': item, 'type': 'folder'})
        
        # Sort items: folders first, then files, both alphabetically by name
        items.sort(key=lambda x: (x['type'] == 'file', x['name'].lower()))
        
        return jsonify({'items': items, 'path': subpath})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download/<path:filepath>')
def download_file(filepath):
    return send_from_directory('downloads', filepath)

@app.route('/rename', methods=['POST'])
def rename_file():
    try:
        data = request.json
        filepath = data['filepath']
        
        full_path = os.path.join('downloads', filepath)
        if not os.path.exists(full_path):
            return jsonify({'status': 'error', 'message': 'File not found'})
        
        # Get directory and filename
        dir_path = os.path.dirname(full_path)
        filename = os.path.basename(full_path)
        
        # Add Z prefix
        new_filename = 'Z' + filename
        new_path = os.path.join(dir_path, new_filename)
        
        # Rename the file
        os.rename(full_path, new_path)
        
        return jsonify({'status': 'success', 'message': 'File renamed successfully'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

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