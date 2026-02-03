from cli import config_store
from cli.commands import config
import pytest

@pytest.fixture()
def mock_config(tmp_path, monkeypatch):
    mock_config_path=tmp_path / "config.json"
    monkeypatch.setattr(config_store, "USER_CONFIG_FILE", mock_config_path)
    yield mock_config_path

def test_set(mock_config):
    config.set("wonderwall", "wav") #you're my wonderwall :p
    dict,eq=config_store.get_config()
    assert dict["output_folder"]=="wonderwall" and dict["audio_format"]=="wav"
