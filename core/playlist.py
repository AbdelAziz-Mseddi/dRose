from . import downloader
from . import utils
###

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
        # print(f"Playlist Title: {plInfo.get('title')}")
        # print(f"Uploader: {plInfo.get('uploader')}")
        # print(f"Track Count: {plInfo.get('playlist_count')}")
        if 'entries' in plInfo:
            # print("\nTrack List:")
            # for track in plInfo['entries']:
            #     print(f"╠ {track.get('title')}, ID={track.get('id')}")
            res={
                "duration":plInfo.get('duration'),
                "uploader":plInfo.get('uploader'),
                "title":plInfo.get('title'),
                "size":plInfo.get('playlist_count'),
                "tracks":[( track.get('title'), track.get('duration')) for track in plInfo['entries']]
            }
            # print(res)
        else:
            res=None
    return res

###Return a list of URLs for all songs in the playlist###

def get_song_urls_from_playlist(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        plInfo=ydl.extract_info(url, download=False)
        if 'entries' in plInfo:
            for track in plInfo['entries']:
                track_urls=[track.get('url') for track in plInfo['entries']]
    return track_urls

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

import os
###DOWNLOAD PLAYLIST###

def download_playlist(url, output_folder=".", audio_format="mp3"):
    urls=get_song_urls_from_playlist(url)
    metadata=get_playlist_info(url)
    title=metadata['title']
    title=utils.sanitize_filename(title)
    utils.create_folder(title)
    for track in urls:
        downloader.download_audio(track, f"{output_folder}/{title}", audio_format)
    

if __name__ == "__main__":
    get_playlist_info("https://music.youtube.com/playlist?list=PLVe3Pb0zUL07V3hhdzjTsaiw7rp7Sg7eD&si=zY7y170jl-TAVuUy")
    print( get_song_urls_from_playlist("https://music.youtube.com/playlist?list=PLVe3Pb0zUL07V3hhdzjTsaiw7rp7Sg7eD&si=zY7y170jl-TAVuUy") ) 
    print(get_song_info("https://music.youtube.com/watch?v=4tJKyfXCDUE&si=aT8MPsNeI_7kDeWa"))
    download_playlist("https://music.youtube.com/playlist?list=PLVe3Pb0zUL04fRNvYJnpg5MFpzcoeT8qb&si=z51v5yyTOxzOZHVu")