import imageio_ffmpeg
import os
import yt_dlp
from . import utils

###Locate and return ffmpeg from imageio-ffmpeg.###

def get_ffmpeg_path():
    path= imageio_ffmpeg.get_ffmpeg_exe()
    return path

ydl_opts = {
    'ffmpeg_location':get_ffmpeg_path(),
    'format':"bestaudio/best",  # Format Selection: Best audio only
    'quiet': True,  # Suppress standard output
    'no_warnings': True,  # Suppress warnings
    'ignoreerrors': True,   # Skip private/deleted videos without stopping
}

###Download original audio file with yt-dlp###

def download_audio(url, output_folder=".", audio_format="mp3"):
    os.makedirs(output_folder, exist_ok=True)
    audio_format=audio_format.lower()
    opts = {**ydl_opts,
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,  # 'mp3', 'm4a', 'flac', 'wav', etc.
                'preferredquality': '192'       # bitrate
        }]}
    with yt_dlp.YoutubeDL(opts) as ydl:
        song=ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(song)
        filename= os.path.splitext(filename)[0] + "." + audio_format
        songName=utils.sanitize_filename(song.get('title'))
        adress= os.path.abspath(filename)
        return adress,songName


if __name__ == "__main__":
    download_audio("https://music.youtube.com/watch?v=4tJKyfXCDUE&si=aT8MPsNeI_7kDeWa")