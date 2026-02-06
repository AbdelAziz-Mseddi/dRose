from core import downloader
from pathlib import Path

def test_download_audio(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    root=tmp_path
    url="https://music.youtube.com/watch?v=84jK2Rzso7M&si=8usd4LeDvBO3ejYB" #3 Doors Down - Here Without You baby
    # damn youtube, i have to mock YoutubeDL
    class FakeYoutubeDL:
        def __init__(self, opts):
            self.opts=opts
        # context manager protocol
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass
        # methods used in core/downloader.py
        def extract_info(self, url, download=True):
            return {
                "title": "Here Without You",
                "ext": "mp3"
            }
        def prepare_filename(self, song):
            path = tmp_path / "Here Without You.mp3"
            path.touch()
            return str(path)
    monkeypatch.setattr("core.downloader.yt_dlp.YoutubeDL", FakeYoutubeDL)
    song_path, song_name=downloader.download_audio(url, root)
    song_path=Path(song_path)
    assert song_path.exists() and song_path.suffix == ".mp3"
    assert song_name is not None and song_name==song_path.stem