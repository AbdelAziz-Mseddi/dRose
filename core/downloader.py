import imageio_ffmpeg
import os
import yt_dlp
ydl_opts = {
    'format':"bestaudio/best",  # Format Selection: Best audio only
    'extract_flat': True,   # Don't download videos, just get valid URLs/titles
    'dump_single_json': True,   # mimic the JSON output format
    'quiet': True,  # Suppress standard output
    'ignoreerrors': True,   # Skip private/deleted videos without stopping
}

###Locate and return ffmpeg from imageio-ffmpeg.###

def get_ffmpeg_path():
    with imageio_ffmpeg.get_ffmpeg_exe() as FFMPEG_PATH :
        return FFMPEG_PATH

###Download original audio file with yt-dlp###

def download_audio_raw(url, output_folder="downloads"):
    os.makedirs(output_folder, exist_ok=True)
    opts = {**ydl_opts, 'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s')}
    with yt_dlp.YoutubeDL(opts) as ydl:
        print(f"Downloading: {url}")
        song=ydl.extract_info(url, download=True)
download_audio_raw("https://music.youtube.com/watch?v=4tJKyfXCDUE&si=aT8MPsNeI_7kDeWa")