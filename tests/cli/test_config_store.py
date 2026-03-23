import json
import pytest
from cli import config_store


@pytest.fixture()
def mock_config(tmp_path, monkeypatch):
    mock_config_path = tmp_path / "config.json"
    mock_default = tmp_path / "default.json"
    mock_default.write_text(
        json.dumps({"output_folder": "/default", "audio_format": "mp3"})
    )
    monkeypatch.setattr(config_store, "USER_CONFIG_FILE", mock_config_path)
    monkeypatch.setattr(config_store, "DEFAULT_CONFIG_FILE", mock_default)
    yield mock_config_path


def test_get_config(mock_config):
    conf, eq = config_store.get_config()
    assert (
        conf["output_folder"] == "/default"
        and conf["audio_format"] == "mp3"
        and eq == True
    )


def test_set_config(mock_config):
    conf, eq = config_store.set_config(
        {"output_folder": "RAGOUJ", "audio_format": None}
    )
    assert (
        conf["output_folder"] == "RAGOUJ"
        and conf["audio_format"] == "mp3"
        and eq == False
    )


def test_get_settinG(mock_config):
    config_store.set_config({"output_folder": "Todd Chavez"})
    assert (
        config_store.get_setting("output_folder") == "Todd Chavez"
        and config_store.get_setting("audio_format") == "mp3"
        and config_store.get_setting("missing") is None
    )


def test_reset_config(mock_config):
    # here, yielding mcok_config_path is necessary because we test if the user configuration file (assigned to "mock_config") exists or not
    config_store.set_config({"output_folder": "x"})
    assert mock_config.exists()
    config_store.reset_config()
    assert not mock_config.exists()
    conf, eq = config_store.get_config()
    assert (
        conf["output_folder"] == "/default"
        and conf["audio_format"] == "mp3"
        and eq is True
    )
