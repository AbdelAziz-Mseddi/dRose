import json
import pytest
from cli import config_store

@pytest.fixture()
def mock_config_paths(tmp_path, monkeypatch):
    mock_user_config = tmp_path / "config.json"
    mock_default_config = tmp_path / "default.json"
    mock_default_config.write_text( json.dumps({"output_folder": "/default", "audio_format": "mp3"}) )
    monkeypatch.setattr(config_store, "USER_CONFIG_FILE", mock_user_config)
    monkeypatch.setattr(config_store, "DEFAULT_CONFIG_FILE", mock_default_config)
    return mock_user_config


def test_get_config(mock_config_paths):
    conf, eq = config_store.get_config()
    assert conf["output_folder"] == "/default" and conf["audio_format"] == "mp3" and eq==True

def test_set_config(mock_config_paths):
    conf, eq = config_store.set_config(
        {"output_folder": "RAGOUJ", "audio_format": None}
    )
    assert conf["output_folder"] == "RAGOUJ" and conf["audio_format"] == "mp3" and eq==False

def test_get_settinG(mock_config_paths):
    config_store.set_config({"output_folder": "Todd Chavez"})
    assert config_store.get_setting("output_folder")=="Todd Chavez" and config_store.get_setting("audio_format")=="mp3" and config_store.get_setting("missing") is None


def test_reset_config(mock_config_paths):
    config_store.set_config({"output_folder": "x"})
    assert mock_config_paths.exists()
    config_store.reset_config()
    assert not mock_config_paths.exists()
    conf, eq = config_store.get_config()
    assert conf["output_folder"] == "/default" and conf["audio_format"] == "mp3" and eq is True