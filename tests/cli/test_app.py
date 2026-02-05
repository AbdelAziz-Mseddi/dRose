from typer.testing import CliTestClient
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


def test_zip(tmp_path, mock_config):
    root=tmp_path
    folder=root / "to_zip"
    folder.mkdir()
    file1= folder / "Salvatore.txt" 
    file2= folder / "Margaret.txt" # 'Cause, baby, if your love is in trouble
    file1.write_text("The View from") # PEAK
    file2.write_text("Halfway Down") # CINEMA
    client=CliTestClient(app.app)
    # without specifying output folder
    result=client.invoke(app.zip, [str(folder)])
    assert result.exit_code==0
    zip_path=root / "to_zip.zip"
    assert zip_path.exists() and zip_path.is_file()
    with zipfile.ZipFile(zip_path, "r") as z:
        names = z.namelist()
        assert "Salvatore.txt" in names
        assert "Margaret.txt" in names
    #with specifying output folder
    result=client.invoke(app.zip, [str(folder), "--output", "Queen"])
    assert result.exit_code==0
    zip_path=root / "Queen.zip"
    assert zip_path.exists() and zip_path.is_file()
    with zipfile.ZipFile(zip_path, "r") as z:
        names = z.namelist()
        assert "Salvatore.txt" in names
        assert "Margaret.txt" in names

    


def test_playlist():
    client=CliTestClient(app.app)
    pass


def test_song():
    client=CliTestClient(app.app)
    pass

