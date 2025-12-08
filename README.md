# 🎵 YouTube Music Downloader

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A **Python-based project** to download **YouTube Music songs and playlists** in one click.  
Includes both a **web app** (FastAPI) and a **command-line interface (CLI)**.

---

## 🚀 Features

- Download **single songs** or **entire playlists**  
- Choose **audio format** (`mp3`, `m4a`, etc.)  
- **Web interface** for easy usage  
- **CLI** for quick terminal downloads  
- Automatic **audio conversion** with **ffmpeg**  
- Optionally bundle multiple songs into a **ZIP file**  
- Progress bar support in CLI using **tqdm**

---

## 🛠 Technologies Used

- **Python 3.10+** – main language  
- **yt-dlp** – core YouTube downloader  
- **ffmpeg** – audio conversion and processing  
- **FastAPI** – backend web framework  
- **Uvicorn** – ASGI server for FastAPI  
- **Jinja2** – HTML templates for frontend  
- **TQDM** – CLI progress bars  
- **Python-multipart** – form data handling  
- **Pydantic** – request validation for API

---

## 💾 Installation

### 1. Clone the repository

git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader


### 2. Create a virtual environment

python -m venv venv


### 3. Activate the virtual environment

**Windows:**
venv\Scripts\activate

**Linux / macOS:**
source venv/bin/activate

### 4. Install dependencies

pip install -r requirements.txt

### 5. Install ffmpeg

- Download ffmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Add it to your system PATH

---

## 🌐 Usage

### Web App

cd web
uvicorn app:app --reload

- Open your browser at `http://127.0.0.1:8000`
- Paste your playlist or song URL, select format, and download 🎶

### CLI

python cli/cli.py --playlist "PLAYLIST_URL" --format mp3

- Download playlists directly from the terminal
- See progress bars for download status

---

## 📁 Project Structure

youtube_downloader/
│
├── core/                  # Core functionality shared by CLI and Web
│   ├── downloader.py      # Functions to download songs/playlists
│   ├── playlist.py        # Playlist metadata fetching
│   └── utils.py           # Helpers: file paths, ZIP creation, sanitizing
│
├── cli/                   # Command-line interface
│   └── cli.py             # Entry point for CLI usage
│
├── web/                   # Web application (FastAPI)
│   ├── app.py             # FastAPI app initialization
│   ├── routers/           # API route definitions
│   │   └── playlist_routes.py
│   ├── services/          # Business logic layer
│   │   └── playlist_service.py
│   ├── templates/         # HTML templates
│   │   └── index.html
│   └── static/            # Frontend assets (CSS/JS)
│       ├── styles.css
│       └── script.js
│
├── downloads/             # Folder where downloaded songs/playlists are saved
├── venv/                  # Python virtual environment (ignored in Git)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

---

## ⚠️ Notes

- Ensure ffmpeg is installed and in your system PATH
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