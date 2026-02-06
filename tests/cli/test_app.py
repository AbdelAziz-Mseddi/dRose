from typer.testing import CliRunner
from cli import config_store
import json
import pytest
from cli import app
import zipfile

@pytest.fixture()
def mock_config(tmp_path, monkeypatch):
    mock_config_path=tmp_path / "config.json"
    mock_default=tmp_path / "default.json"
    mock_default.write_text(json.dumps({"output_folder": str(tmp_path), "audio_format": "mp3"}))
    monkeypatch.setattr(config_store, "USER_CONFIG_FILE", mock_config_path)
    monkeypatch.setattr(config_store, "DEFAULT_CONFIG_FILE", mock_default)
    yield mock_config_path


def test_zip(tmp_path, mock_config, monkeypatch):
    root=tmp_path
    folder=root / "to_zip"
    folder.mkdir()
    file1= folder / "Salvatore.txt" 
    file2= folder / "Margaret.txt" # 'Cause, baby, if your love is in trouble
    file1.write_text("The View from") # PEAK
    file2.write_text("Halfway Down") # CINEMA
    runner = CliRunner()
    # without specifying output folder
    result = runner.invoke(app.app, ["zip", str(folder)])
    assert result.exit_code==0
    zip_path=root / "to_zip.zip"
    base=zip_path.as_posix() # to make the string path use / always
    assert zip_path.exists() and zip_path.is_file()
    with zipfile.ZipFile(zip_path, "r") as z:
        names = z.namelist()
        assert f"{base}/Salvatore.txt" in names
        assert f"{base}/Margaret.txt" in names
    #with specifying output folder
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app.app, ["zip", str(folder), "--output", "Queen"])
    assert result.exit_code==0
    zip_path=root / "Queen.zip"
    base=zip_path.as_posix()
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
    assert calls["url"] == "https://music.youtube.com/playlist?list=OLAK5uy_kPmvbW7SIcqYc2_RHCnaOYtImxo5vnZTg&si=buKDEbMt5WntFoly"
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
        return out+"Fijibi"+fmt, "Fijibi"
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
    assert calls["url"] == "https://music.youtube.com/watch?v=E6no86tg0fQ&si=-Q5I6Zsft9YWU-nq" # hemli le ma kedni :3
    assert calls["output"] == str(tmp_path)  # because mock_config sets output_folder 
    assert calls["format"] == "mp3"