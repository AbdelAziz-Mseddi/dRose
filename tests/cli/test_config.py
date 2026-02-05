from cli import config_store
from cli.commands import config
from typer.testing import CliTestClient
import pytest
import json

@pytest.fixture()
def mock_config(tmp_path, monkeypatch):
    mock_config_path=tmp_path / "config.json"
    mock_default=tmp_path / "default.json"
    mock_default.write_text(json.dumps({"output_folder": "/default", "audio_format": "mp3"}))
    monkeypatch.setattr(config_store, "USER_CONFIG_FILE", mock_config_path)
    monkeypatch.setattr(config_store, "DEFAULT_CONFIG_FILE", mock_default)
    yield mock_config_path

def test_set(mock_config):
    client=CliTestClient(config.app)
    result=client.invoke(config.set, ["--output-folder", "wonderwall", "--audio-format", "wav"]) #you're my wonderwall :p
    assert result.exit_code==0
    config_dict,eq=config_store.get_config()
    assert config_dict["output_folder"]=="wonderwall" and config_dict["audio_format"]=="wav" and len(config_dict)==2 and eq==False
    result=client.invoke(config.set, ["--output-folder", "sarah lynn"])
    assert result.exit_code==0
    config_dict,eq=config_store.get_config()
    assert config_dict["output_folder"]=="sarah lynn" and len(config_dict)==2 and eq==False  

def test_reset(mock_config):
    client=CliTestClient(config.app)
    result=client.invoke(config.reset)
    assert result.exit_code==0
    config_dict,eq=config_store.get_config()
    assert eq==True and len(config_dict)==2