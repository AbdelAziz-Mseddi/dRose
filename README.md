<div align="center">
  <img src="assets/dRose.png" alt="dragoulaRose Logo" width="200" height="auto">
  
  <h1>dRose v1.1.1</h1>
  
  <p>
    <b>The Ultimate YouTube Music Downloader</b>
  </p>

  [![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
</div>

---

A **Python-based CLI tool** to download **YouTube Music songs and playlists** in one click.

---

## 🚀 Features

- Download **single songs** or **entire playlists**  
- Choose **audio format** (`mp3`, `m4a`, etc.)  
- **CLI** for quick terminal downloads  
- Automatic **audio conversion** with **ffmpeg**  
- Optionally bundle multiple songs into a **ZIP file**  

---

## 🛠 Technologies Used

- **Python 3.12+** – main language  
- **yt-dlp** – core YouTube downloader  
- **ffmpeg** – audio conversion and processing  
- **imageio-ffmpeg** – Bundled FFmpeg binary (No installation required)

---

## 💾 Installation

### 1. Install pipx

`pipx` installs Python CLI tools globally so they work from any terminal without activating a virtual environment.

**Linux / macOS:**
```bash
sudo apt install pipx   # Debian/Ubuntu
pipx ensurepath         # adds ~/.local/bin to PATH (restart terminal after)
```

**Windows:**
```powershell
python -m pip install --user pipx
python -m pipx ensurepath
```

### 2. Clone the repository

```bash
git clone https://github.com/AbdelAziz-Mseddi/dRose.git
cd dRose
```

### 3. Install drose

**For regular use:**
```bash
pipx install .
```

**For development (editable install — code changes apply immediately):**
```bash
pipx install --editable .
```

**For development with extras (tests, web features):**
```bash
pipx install --editable ".[dev]"
```

After installation, `drose` is available globally from any directory.

---

## 🌐 Usage

### Getting Started

Run `drose` without arguments to see the welcome screen and quick start guide:

```bash
drose
```
<img src="assets/drose_terminal.png" alt="welcome" height="400px" width=auto>

### Available Commands

#### Download a Playlist

```bash
drose playlist "PLAYLIST_URL" [OPTIONS]
```

**Options:**
- `-o, --output_dir PATH` - Output directory (defaults to config)
- `-f, --format FORMAT` - Audio format: mp3, m4a, etc. (defaults to config)
- `-l, --list` - Show playlist information without downloading
- `-a, --all` - Show detailed info (duration, size, artists)

**Examples:**
```bash
# Download playlist with default settings
drose playlist "https://youtube.com/playlist?list=..."

# List playlist songs without downloading
drose playlist "PLAYLIST_URL" --list

# Download with custom format and output
drose playlist "PLAYLIST_URL" -f m4a -o ./downloads
```

#### Download a Song

```bash
drose song "SONG_URL" [OPTIONS]
```

**Options:**
- `-o, --output_dir PATH` - Output directory (defaults to config)
- `-f, --format FORMAT` - Audio format (defaults to config)
- `-l, --list` - Show song information without downloading
- `-a, --all` - Show additional info (release date, estimated size)

**Examples:**
```bash
# Download a single song
drose song "https://youtube.com/watch?v=..."

# Show song info without downloading
drose song "SONG_URL" --list --all
```

#### Configuration Management

```bash
# View current configuration
drose config show

# Set default output folder
drose config set --output-folder "./downloads"

# Set default audio format
drose config set --audio-format "mp3"

# Set both in one command
drose config set --output-folder "./downloads" --audio-format "m4a"

# Read a single setting
drose config get output_folder

# Reset to default configuration
drose config reset
```

Config values are merged from:
- Defaults: `cli/config.default.json`
- User overrides: `~/.drose/config.json`

#### System Health Check

```bash
# Check if all dependencies are properly installed
drose doctor
```

#### Zip Downloaded Content

```bash
# Zip a folder (useful for downloaded playlists)
drose zip "./downloads/playlist-name" -o "./archive.zip"
```

### Other Options

```bash
# Show version
drose --version

# Show help
drose --help

# Get help for a specific command
drose playlist --help
```

---

## ✅ Testing

Run tests locally:

```bash
pytest -q
```

Optional coverage report:

```bash
pytest --cov=cli --cov=core --cov-report=term-missing
```

---

## 📁 Project Structure

```text
dRose/
│
├── assets/             # Project assets (logos, ASCII art)
|
├── cli/                # Command-line interface
│   ├── app.py          # Main CLI entry point
│   ├── config_store.py # Configuration management
│   ├── config.default.json
│   └── commands/       # CLI command modules
│       ├── config.py   # Config command
│       └── doctor.py   # Doctor/health check command
│
├── core/               # Core functionality and business logic
│   ├── __init__.py
│   ├── downloader.py   # Main YouTube downloader using yt-dlp
│   ├── playlist.py     # Playlist parsing and extraction
│   └── utils.py        # Utility functions
│
├── tests/              # Test suite
│   ├── cli/
│   └── core/
│
├── pyproject.toml      # Project configuration
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```
---

## 📋 Future Plans

- **Web interface** – A FastAPI-based web app with UI is planned for future releases
- **Enhanced features** – Improved UI/UX and additional download options
- **Download history** – Track previously downloaded content
- **Suggest new Songs** - Based on previous downloads
- **Playlist management** – Organize and manage playlists

---

## ⚠️ Notes

- For Windows users, `.DS_Store` files are not relevant

---

## 🧰 Troubleshooting

- Run `drose doctor` to verify system compatibility and required dependencies.
- Confirm Python version is `3.12+`.
- If FFmpeg is not available system-wide, `imageio-ffmpeg` is used as a fallback.
- Some downloads may fail due to unavailable/private videos, rate limits, or network restrictions.

---

## 🤝 Contributing

Feel free to:

- Add new features
- Improve UI/UX
- Optimize download speed
- Report issues or submit pull requests

---

## 📜 License

This project is licensed under the MIT License.