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

def test_download_playlist(tmp_path):
    root=tmp_path
    url="https://music.youtube.com/playlist?list=PLVe3Pb0zUL05U3MfDdxMvyOHdwE7hYP2S&si=9i-hLHd9ydd6kPUc" #i don't want my code to crash
    output=root
    playlist.download_playlist(url, str(output))
    playlist_path=tmp_path / "VHS"
    assert playlist_path.exists() and playlist_path.is_dir()
    for file in playlist_path.iterdir():
        assert file.is_file() and file.suffix==".mp3"