import json
from pathlib import Path

# Default config stored alongside this module
DEFAULT_CONFIG_FILE = Path(__file__).with_name("config.default.json")
# User overrides stored in home directory for persistence
USER_CONFIG_FILE = Path.home() / ".drose" / "config.json"


def _read_json(path: Path) -> dict:
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_config() -> dict:
    """Return merged config: defaults overridden by user settings"""
    defaults = _read_json(DEFAULT_CONFIG_FILE)
    overrides = _read_json(USER_CONFIG_FILE)
    merged = {**defaults, **overrides}
    return (merged,defaults==merged)


def set_config(updates: dict) -> dict:
    """Update user overrides and return merged config"""
    current = _read_json(USER_CONFIG_FILE)
    current.update({k: v for k, v in updates.items() if v is not None})
    _write_json(USER_CONFIG_FILE, current)
    return get_config()


def get_setting(name: str):
    return get_config().get(name)
