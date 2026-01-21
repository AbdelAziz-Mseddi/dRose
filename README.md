<div align="center">
  <img src="assets/dRose.png" alt="dragoulaRose Logo" width="200" height="auto">
  
  <h1>dragRose</h1>
  
  <p>
    <b>The Ultimate YouTube Music Downloader</b>
  </p>

  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
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
- Progress bar support using **tqdm**

---

## 🛠 Technologies Used

- **Python 3.10+** – main language  
- **yt-dlp** – core YouTube downloader  
- **ffmpeg** – audio conversion and processing  
- **imageio-ffmpeg** – Bundled FFmpeg binary (No installation required)
- **TQDM** – CLI progress bars

---

## 💾 Installation

### 1. Clone the repository

git clone https://github.com/yourusername/youtube-downloader.git
cd dRose


### 2. Create a virtual environment

python -m venv venv


### 3. Activate the virtual environment

**Windows:**
venv\Scripts\activate

**Linux / macOS:**
source venv/bin/activate

### 4. Install dependencies

pip install -r requirements.txt

---

## 🌐 Usage

### CLI

```bash
drose playlist "PLAYLIST_URL" --format mp3
```

- Download playlists directly from the terminal
- See progress bars for download status

---

## 📁 Project Structure

```text
dRose/
│
├── assets/             # Project assets (logos, images)
│
├── cli/                # Command-line interface
│   ├── app.py          # Main CLI entry point
│   ├── config_store.py # Configuration management
│   ├── config.default.json
│   └── commands/       # CLI command modules
│       ├── config.py   # Config command
│       └── doctor.py   # Doctor command
│
├── core/               # Core functionality and business logic
│   ├── __init__.py
│   ├── downloader.py   # Main YouTube downloader using yt-dlp
│   ├── playlist.py     # Playlist parsing and extraction
│   └── utils.py        # Utility functions
│
├── pyproject.toml      # Project configuration
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```
---

## 📋 Future Plans

- **Web interface** – A FastAPI-based web app is planned for future releases

---

## ⚠️ Notes

- The project uses a virtual environment for dependency management
- For Windows users, `.DS_Store` files are not relevant

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