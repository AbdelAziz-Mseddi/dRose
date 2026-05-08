from typer.testing import CliRunner
from cli import config_store
import json
import pytest
from cli import app
import zipfile


@pytest.fixture()
def mock_config(tmp_path, monkeypatch):
    mock_config_path = tmp_path / "config.json"
    mock_default = tmp_path / "default.json"
    mock_default.write_text(
        json.dumps({"output_folder": str(tmp_path), "audio_format": "mp3"})
    )
    monkeypatch.setattr(config_store, "USER_CONFIG_FILE", mock_config_path)
    monkeypatch.setattr(config_store, "DEFAULT_CONFIG_FILE", mock_default)
    yield mock_config_path


def test_zip(tmp_path, mock_config, monkeypatch):
    root = tmp_path
    folder = root / "to_zip"
    folder.mkdir()
    file1 = folder / "Salvatore.txt"
    file2 = folder / "Margaret.txt"  # 'Cause, baby, if your love is in trouble
    file1.write_text("The View from")  # PEAK
    file2.write_text("Halfway Down")  # CINEMA
    runner = CliRunner()
    # without specifying output folder
    result = runner.invoke(app.app, ["zip", str(folder)])
    assert result.exit_code == 0
    zip_path = root / "to_zip.zip"
    base = folder.as_posix()  # to make the string path use / always
    assert zip_path.exists() and zip_path.is_file()
    with zipfile.ZipFile(zip_path, "r") as z:
        names = z.namelist()
        assert f"{base}/Salvatore.txt"[1::] in names
        assert f"{base}/Margaret.txt"[1::] in names
    # with specifying output folder
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app.app, ["zip", str(folder), "--output", "Queen"])
    assert result.exit_code == 0
    zip_path = root / "Queen.zip"
    base = folder.as_posix()
    assert zip_path.exists() and zip_path.is_file()
    with zipfile.ZipFile(zip_path, "r") as z:
        names = z.namelist()
        assert f"{base}/Salvatore.txt"[1::] in names
        assert f"{base}/Margaret.txt"[1::] in names


def test_playlist(mock_config, monkeypatch, tmp_path):
    calls = {}

    # mocking the original download_playlist to avoid hitting YouTube and encountring network or rate limits problems
    # makes sure the cli passed the right URL, output folder and format
    # core tests already use the real download functions
    def fake_download_playlist(url, out, fmt):
        calls["url"] = url
        calls["output"] = out
        calls["format"] = fmt

    monkeypatch.setattr(app, "download_playlist", fake_download_playlist)
    runner = CliRunner()
    result = runner.invoke(
        app.app,
        [
            "playlist",
            "https://music.youtube.com/playlist?list=OLAK5uy_kPmvbW7SIcqYc2_RHCnaOYtImxo5vnZTg&si=buKDEbMt5WntFoly",
        ],
    )
    assert result.exit_code == 0
    assert (
        calls["url"]
        == "https://music.youtube.com/playlist?list=OLAK5uy_kPmvbW7SIcqYc2_RHCnaOYtImxo5vnZTg&si=buKDEbMt5WntFoly"
    )
    assert calls["output"] == str(tmp_path)  # because mock_config sets output_folder
    assert calls["format"] == "mp3"


def test_song(mock_config, monkeypatch, tmp_path):
    calls = {}

    # mocking the original download_audio to avoid hitting YouTube and encountring network or rate limits problems
    # makes sure the cli passed the right URL, output folder and format
    # core tests already use the real download functions
    def fake_download_audio(url, out, fmt):
        calls["url"] = url
        calls["output"] = out
        calls["format"] = fmt
        # replacing function must satisfy the same interface and contract that the real function has for the code paths being tested
        return out + "Fijibi" + fmt, "Fijibi"

    monkeypatch.setattr(app, "download_audio", fake_download_audio)
    runner = CliRunner()
    result = runner.invoke(
        app.app,
        [
            "song",
            "https://music.youtube.com/watch?v=E6no86tg0fQ&si=-Q5I6Zsft9YWU-nq",
        ],
    )
    assert result.exit_code == 0
    assert (
        calls["url"]
        == "https://music.youtube.com/watch?v=E6no86tg0fQ&si=-Q5I6Zsft9YWU-nq"
    )  # hemli le ma kedni :3
    assert calls["output"] == str(tmp_path)  # because mock_config sets output_folder
    assert calls["format"] == "mp3"


def test_song_multiple_urls(mock_config, monkeypatch, tmp_path):
    calls = []

    def fake_download_audio(url, out, fmt):
        calls.append({"url": url, "output": out, "format": fmt})
        return out + "Fijibi" + fmt, "Fijibi"

    monkeypatch.setattr(app, "download_audio", fake_download_audio)
    runner = CliRunner()
    urls = [
        "https://music.youtube.com/watch?v=E6no86tg0fQ",
        "https://music.youtube.com/watch?v=kJQP7kiw5Fk",
    ]
    result = runner.invoke(app.app, ["song", *urls])
    assert result.exit_code == 0
    assert len(calls) == 2
    assert [call["url"] for call in calls] == urls
    for call in calls:
        assert call["output"] == str(tmp_path)
        assert call["format"] == "mp3"


def test_playlist_prompt(mock_config, monkeypatch, tmp_path):
    calls = []

    urls = [
        "https://music.youtube.com/watch?v=one",
        "https://music.youtube.com/watch?v=two",
        "https://music.youtube.com/watch?v=three",
    ]

    def fake_get_playlist_info(url):
        return {"title": "Prompt Playlist", "size": 3, "tracks": []}

    def fake_get_urls(url):
        return urls

    def fake_get_song_info(url):
        mapping = {urls[0]: "One", urls[1]: "Two", urls[2]: "Three"}
        return {"title": mapping[url], "duration": 200}

    def fake_download_audio(url, out, fmt):
        calls.append({"url": url, "output": out, "format": fmt})
        return out + "Fijibi" + fmt, "Fijibi"

    # Patch core functions so `is_song_url` and other imports use the fakes
    import core.playlist as core_playlist
    import core.downloader as core_downloader

    monkeypatch.setattr(core_playlist, "get_playlist_info", fake_get_playlist_info)
    monkeypatch.setattr(core_playlist, "get_song_urls_from_playlist", fake_get_urls)
    monkeypatch.setattr(core_playlist, "get_song_info", fake_get_song_info)
    monkeypatch.setattr(core_downloader, "download_audio", fake_download_audio)
    # Also patch names imported into the CLI app module
    monkeypatch.setattr(app, "get_playlist_info", fake_get_playlist_info)
    monkeypatch.setattr(app, "get_song_urls_from_playlist", fake_get_urls)
    monkeypatch.setattr(app, "get_song_info", fake_get_song_info)
    monkeypatch.setattr(app, "download_audio", fake_download_audio)

    runner = CliRunner()
    # Answers: yes, no, yes
    result = runner.invoke(
        app.app,
        [
            "playlist",
            "https://music.youtube.com/playlist?list=OLAK5uy_example",
            "-p",
        ],
        input="y\nn\ny\n",
    )
    assert result.exit_code == 0
    # Only two downloads should have been called (first and third)
    assert len(calls) == 2
    for call in calls:
        assert call["output"].startswith(str(tmp_path))
        assert call["format"] == "mp3"
