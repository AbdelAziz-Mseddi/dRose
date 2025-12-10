import yt_dlp
###Retrieve playlist title, number of songs, and every song title###

def get_playlist_info(url):
    ydl_opts = {
        'extract_flat': True,   # Don't download videos, just get valid URLs/titles
        'dump_single_json': True,   # mimic the JSON output format
        'quiet': True,  # Suppress standard output
        'ignoreerrors': True,   # Skip private/deleted videos without stopping
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        plInfo=ydl.extract_info(url, download=False)
        print(f"Playlist Title: {plInfo.get('title')}")
        print(f"Uploader: {plInfo.get('uploader')}")
        print(f"Track Count: {plInfo.get('playlist_count')}")
        if 'entries' in plInfo:
            print("\nTrack List:")
            for track in plInfo['entries']:
                print(f"╠ {track.get('title')}, ID={track.get('id')}")
get_playlist_info("https://music.youtube.com/playlist?list=PLVe3Pb0zUL07V3hhdzjTsaiw7rp7Sg7eD&si=zY7y170jl-TAVuUy")