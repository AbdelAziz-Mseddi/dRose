import imageio_ffmpeg
import os
import yt_dlp

###Locate and return ffmpeg from imageio-ffmpeg.###

def get_ffmpeg_path():
    path= imageio_ffmpeg.get_ffmpeg_exe()
    return path

ydl_opts = {
    'ffmpeg_location':get_ffmpeg_path(),
    'format':"bestaudio/best",  # Format Selection: Best audio only
    'quiet': True,  # Suppress standard output
    'ignoreerrors': True,   # Skip private/deleted videos without stopping
}

###Download original audio file with yt-dlp###

def download_audio_raw(url, output_folder="rawDownloads"):
    os.makedirs(output_folder, exist_ok=True)
    opts = {**ydl_opts, 'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s')}
    with yt_dlp.YoutubeDL(opts) as ydl:
        print(f"Downloading: {url}")
        song=ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(song)
        songName=song.get('title')
        return os.path.abspath(filename),songName

import subprocess
###Convert downloaded audio → MP3 using ffmpeg###

def convert_to_mp3(input_path, songName, output_folder):
    os.makedirs(f"{output_folder}", exist_ok=True)
    output_path=f"{output_folder}\{songName}.mp3"
    ffmpeg_exe=get_ffmpeg_path()
    cmnd = [
        ffmpeg_exe, # The program to run
        '-y',   # Overwrite output file without asking
        '-i', input_path,   # Input file
        '-acodec', 'libmp3lame',    # Audio codec (mp3)
        '-q:a', '2',    # Quality (VBR scale 0-9, 2 is standard
        output_path     # Output file
    ]
    exec=subprocess.run(
        cmnd,
        check=True,     # Capture standard output
        stdout=subprocess.PIPE,     # Capture standard output
        stderr=subprocess.PIPE,     # Capture error/log output (FFmpeg logs to stderr!)
        text=True,   # Return strings instead of bytes
        encoding='utf-8',       # Force UTF-8 encoding
        errors='replace'
    )
    

###Wrapper to donwload a single song###
def download_single(url, output_folder="downloads"):
    adress,songName=download_audio_raw(url)
    convert_to_mp3(adress, songName, output_folder)

if __name__ == "__main__":
    download_single("https://music.youtube.com/watch?v=4tJKyfXCDUE&si=aT8MPsNeI_7kDeWa")