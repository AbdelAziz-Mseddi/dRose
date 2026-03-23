from cli import config_store
from cli.commands import config
from typer.testing import CliRunner
import pytest
import json


@pytest.fixture()
def mock_config(tmp_path, monkeypatch):
    mock_config_path = tmp_path / "config.json"
    mock_default = tmp_path / "default.json"
    mock_default.write_text(
        json.dumps({"output_folder": "/default", "audio_format": "mp3"})
    )
    monkeypatch.setattr(config_store, "USER_CONFIG_FILE", mock_config_path)
    monkeypatch.setattr(config_store, "DEFAULT_CONFIG_FILE", mock_default)
    yield mock_config_path  # not used in tests directly but have to yield something (or None) for pytest to run successfully


def test_set(mock_config):
    runner = CliRunner()
    result = runner.invoke(
        config.app,
        ["set", "--output-folder", "wonderwall", "--audio-format", "wav"],
    )
    assert result.exit_code == 0
    config_dict, eq = config_store.get_config()
    assert (
        config_dict["output_folder"] == "wonderwall"
        and config_dict["audio_format"] == "wav"
        and len(config_dict) == 2
        and eq == False
    )
    result = runner.invoke(config.app, ["set", "--output-folder", "sarah lynn"])
    assert result.exit_code == 0
    config_dict, eq = config_store.get_config()
    assert (
        config_dict["output_folder"] == "sarah lynn"
        and len(config_dict) == 2
        and eq == False
    )


def test_reset(mock_config):
    # we don't need to return mock_default or mock_config_path in mock_config because config_store.get_config doesn't need
    # their values directly but it accesses them using the monkeypatch
    runner = CliRunner()
    result = runner.invoke(config.app, ["reset"])
    assert result.exit_code == 0
    config_dict, eq = config_store.get_config()
    assert eq == True and len(config_dict) == 2
