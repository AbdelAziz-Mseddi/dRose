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
- **imageio-ffmpeg** – Bundled FFmpeg binary (No installation required)
- **Uvicorn** – ASGI server for FastAPI  
- **Jinja2** – HTML templates for frontend  
- **TQDM** – CLI progress bars  
- **Python-multipart** – form data handling  
- **Pydantic** – request validation for API

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

```text
youtube_downloader/
│
├── assets/             # Project assets (logos, iamges)
│
├── core/               # Core functionality and business logic
│   ├── downloader.py   # Main YouTube downloader using yt-dlp
│   ├── playlist.py     # Playlist parsing and extraction
│   └── utils.py        # Utility functions
│
├── cli/                # Command-line interface
│   └── cli.py          # Main CLI entry point
│
├── web/                # Web application
│   ├── app.py          # FastAPI application
│   ├── templates/      # HTML templates
│   └── static/         # CSS and JS files
│
├── downloads/          # Folder for downloaded files
├── venv/               # Virtual environment (ignored in Git)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```
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