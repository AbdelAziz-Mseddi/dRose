from core import playlist
from pathlib import Path
def test_get_playlist_info():
    url="https://music.youtube.com/playlist?list=PLVe3Pb0zUL05U3MfDdxMvyOHdwE7hYP2S&si=9i-hLHd9ydd6kPUc" #example of palylist
    to_test=playlist.get_playlist_info(url)
    assert len(to_test)==5

def test_get_song_urls_from_playlist():
    url="https://music.youtube.com/playlist?list=PLVe3Pb0zUL05U3MfDdxMvyOHdwE7hYP2S&si=9i-hLHd9ydd6kPUc" #i hope this playlists doesn't change or disappear
    to_test=playlist.get_song_urls_from_playlist(url)
    for url in to_test:
        assert url.startswith("https://music.youtube.com/")

def test_download_playlist(tmp_path, monkeypatch):
    root=tmp_path
    url="https://music.youtube.com/playlist?list=PLVe3Pb0zUL05U3MfDdxMvyOHdwE7hYP2S&si=9i-hLHd9ydd6kPUc" #i don't want my code to crash
    output=root
    music=["Nafs", "Vodka", "على باب السيما", "Dance with The Devil"]
    # your usual mocking, sir?
    # functions used in core/playlist.py
    # i know i don't need to mock get_song_urls_from_playlist and get_playlist_info but no need go through them again
    def mock_urls(url):
        return [ "https://music.youtube.com/watch?v=lxBupPZBCb0&si=kjxqg5mVaPZE79vn", #NAFS
                "https://music.youtube.com/watch?v=f7c88WJzQTY&si=yKt0JB3hWA8dPFsR", #vodka
                "https://music.youtube.com/watch?v=kPouhuOAzi0&si=IQFmEuK_Lx67YEjO", #Raphinha
                 "https://music.youtube.com/watch?v=Ef1fy2k_EYI&si=BPDzVDgJ02ADXiCD" #Dance With The Devil
                ] 
    def mock_info(url):
        return {
            "duration": 1031,
            "uploader": "Free Palestine",
            "title": "It's A Meee Mario",
            "size": 4,
            "tracks":[  ( "Nafs", 205, "EMP1RE" ),
                        ( "Vodka", 261, "Al Selem Band" ),
                        ( "على باب السيما", 152, "Cairokee" ),
                        ( "Dance with The Devil", 413, "Immoral Technique" )
                      ]
        }
    class FakeYoutubeDL:
        def __init__(self, opts):
            self.opts=opts
            self._song_iter=self._iter_songs()
            self._path_iter=self._iter_paths()
        # context manager protocol
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass
        def _iter_songs(self):
            for track in music:
                yield {
                    "title": track,
                    "ext": "mp3"
                }
        def _iter_paths(self):
            for track in music:
                path=tmp_path/track
                path.touch()
                yield str(path)
        # methods used in core/downloader.py
        def extract_info(self, url, download=True):
            return next(self._song_iter)
        def prepare_filename(self, song):
            return next(self._path_iter)
    monkeypatch.setattr("core.playlist.get_song_urls_from_playlist", mock_urls)
    monkeypatch.setattr("core.playlist.get_playlist_info", mock_info)
    monkeypatch.setattr("core.downloader.yt_dlp.YoutubeDL", FakeYoutubeDL)
    playlist.download_playlist(url, str(output))
    playlist_path=tmp_path / "It's A Meee Mario"
    assert playlist_path.exists() and playlist_path.is_dir()
    for file in playlist_path.iterdir():
        assert file.is_file() and file.suffix==".mp3"
#So when the devil wants to dance with you, you better say never
#Because the dance with the devil might last you forever