from core import utils
from pathlib import Path
import zipfile

def test_create_folder(tmp_path):
    root=tmp_path
    name="diane"
    nguyen=utils.create_folder(name,root)
    assert nguyen.exists() and nguyen.is_dir() and nguyen=="diane"

def test_zip_folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    root=tmp_path
    folder=root / "to_zip" #works because tmp_path is of type pathlib.Path and / is overloaded
    folder.mkdir()
    file1= folder / "Lessa.txt"
    file2= folder / "bahinlha.txt"
    file1.write_text("V for Vendetta")
    file2.write_text("Leon: The Professional")
    utils.zip_folder(folder,"archived")
    zip_path=tmp_path / "archived.zip"
    assert zip_path.exists() and zip_path.is_file()
    with zipfile.ZipFile(zip_path, "r") as z:
        names = z.namelist()
        assert "Lessa.txt" in names
        assert "bahinlha.txt" in names