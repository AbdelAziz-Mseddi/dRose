from core import downloader
import os
from pathlib import Path

def test_download_audio(tmp_path):
    root=tmp_path
    url="https://music.youtube.com/watch?v=84jK2Rzso7M&si=8usd4LeDvBO3ejYB" #3 Doors Down - Here Without You Baby
    song_path, song_name=downloader.download_audio(url, root)
    song_path=Path(song_path)
    assert song_path.exists() and song_path.suffix == ".mp3"
    assert song_name is not None and song_name==song_path.stem