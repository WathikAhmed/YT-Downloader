# YouTube Downloader

Simple web app to download YouTube videos.

## Setup

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Run the app:
```bash
python3 app.py
```

3. Open http://127.0.0.1:8080 in your browser

4. Paste a YouTube URL and click Download

Videos will be saved in the `downloads/` folder.

## Access from Other Devices

To use the app from your phone or other devices on the same network:

1. Find your computer's IP address:
   - **Mac/Linux**: `ifconfig | grep "inet " | grep -v 127.0.0.1`
   - **Windows**: `ipconfig`

2. On your phone/device, open a browser and go to:
   `http://YOUR_IP_ADDRESS:8080`
   
   Example: `http://192.168.0.71:8080`

3. Videos will still download to your computer's `downloads/` folder