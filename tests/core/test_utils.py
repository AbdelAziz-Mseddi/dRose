from core import utils
from pathlib import Path

def test_create_folder(where):
    root=where
    name="diane"
    nguyen=utils.create_folder(name,root)
    assert nguyen.exists() and nguyen.is_dir() and nguyen=="diane"