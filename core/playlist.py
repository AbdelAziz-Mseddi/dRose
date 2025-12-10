ydl_opts = {
        'extract_flat': True,   # Don't download videos, just get valid URLs/titles
        'dump_single_json': True,   # mimic the JSON output format
        'quiet': True,  # Suppress standard output
        'ignoreerrors': True,   # Skip private/deleted videos without stopping
    }

import yt_dlp
###Retrieve playlist title, number of songs, and every song title###

def get_playlist_info(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        plInfo=ydl.extract_info(url, download=False)
        print(f"Playlist Title: {plInfo.get('title')}")
        print(f"Uploader: {plInfo.get('uploader')}")
        print(f"Track Count: {plInfo.get('playlist_count')}")
        if 'entries' in plInfo:
            print("\nTrack List:")
            for track in plInfo['entries']:
                print(f"╠ {track.get('title')}, ID={track.get('id')}")
    res={
        "title":plInfo.get('title'),
        "size":plInfo.get('playlist_count'),
        "tracks":[track.get('title') for track in plInfo['entries']]
    }
    print(res)
    return res
get_playlist_info("https://music.youtube.com/playlist?list=PLVe3Pb0zUL07V3hhdzjTsaiw7rp7Sg7eD&si=zY7y170jl-TAVuUy")

###Return a list of URLs for all songs in the playlist###

def get_song_urls_from_playlist(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        plInfo=ydl.extract_info(url, download=False)
        if 'entries' in plInfo:
            for track in plInfo['entries']:
                track_urls=[track.get('url') for track in plInfo['entries']]
    return track_urls
print( get_song_urls_from_playlist("https://music.youtube.com/playlist?list=PLVe3Pb0zUL07V3hhdzjTsaiw7rp7Sg7eD&si=zY7y170jl-TAVuUy") ) 

###Retrieve data for a single song (title, duration, etc.)###

def get_song_info(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        songInfo=ydl.extract_info(url, download=False)
        res={
            'title':songInfo.get('title'),
            'duration':songInfo.get('duration'),
            'uploader':songInfo.get('uploader')
        }
    return res
print(get_song_info("https://music.youtube.com/watch?v=4tJKyfXCDUE&si=aT8MPsNeI_7kDeWa"))