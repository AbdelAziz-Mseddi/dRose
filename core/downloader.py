import imageio_ffmpeg
import os
import yt_dlp
from rich.progress import BarColumn, DownloadColumn, Progress, SpinnerColumn, TextColumn, TimeRemainingColumn
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
    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},  # Use multiple clients
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',  # Modern user agent
}

###Download original audio file with yt-dlp###

def download_audio(url, output_folder=".", audio_format="mp3"):
    url = utils.ensure_url_scheme(url)
    os.makedirs(output_folder, exist_ok=True)
    audio_format=audio_format.lower()
    opts = {**ydl_opts,
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,  # 'mp3', 'm4a', 'flac', 'wav', etc.
                'preferredquality': '192'       # bitrate
        }]}
    # for progress bar
    progress_state = {'set_title': False}
    # fucntion that receives data from yt-dlp and uses it to update the progress bar
    # it gives Rich data about the downlaod status and number of bytes
    # Rich handles calculating percentage and the other things, it only sens it updates
    def progress_hook(data):
        status=data.get('status')
        info=data.get('info_dict', {})
        if not progress_state['set_title']:
            title=info.get('title')
            if title:
                progress.update(song_bar, description=title)
                progress_state['set_title'] = True
        if status == 'downloading':
            downloaded=data.get('downloaded_bytes', 0)
            total=data.get('total_bytes') or data.get('total_bytes_estimate')
            if total:
                progress.update(song_bar, total=total, completed=downloaded)
            else:
                progress.update(song_bar, completed=downloaded)
        elif status == 'finished':
            total=data.get('total_bytes') or data.get('total_bytes_estimate')
            if total:
                progress.update(song_bar, total=total, completed=total)
    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TimeRemainingColumn(),
        transient=False,
    ) as progress:
        song_bar=progress.add_task("Downloading", total=None)
        # for downloading
        opts = {**opts, 'progress_hooks': [progress_hook]}
        with yt_dlp.YoutubeDL(opts) as ydl:
            song = ydl.extract_info(url, download=True)
            if song is None :
                raise RuntimeError("Failed to hit YouTube correctly or wrong URL")
            filename = ydl.prepare_filename(song)
            filename= os.path.splitext(filename)[0] + "." + audio_format
            songName=utils.sanitize_filename(song.get('title'))
            adress= os.path.abspath(filename)
            return adress,songName


if __name__ == "__main__":
    download_audio("https://music.youtube.com/watch?v=4tJKyfXCDUE&si=aT8MPsNeI_7kDeWa")