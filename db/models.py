from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()
def utc_now():
    """Return current UTC datetime"""
    return datetime.now(timezone.utc)

class Song(Base):
    __tablename__ = "songs"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artist = Column(String)
    duration = Column(Float)  # in seconds
    youtube_id = Column(String, unique=True, nullable=False)
    youtube_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now) # utc_now without parentheses because we pass the function not its result when the script is executed :p

class Playlist(Base):
    __tablename__ = "playlists"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    youtube_id = Column(String, unique=True, nullable=False)
    youtube_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

class DownloadRecord(Base):
    __tablename__ = "download_records"
    
    id = Column(Integer, primary_key=True)
    song_id = Column(Integer)  # FK to Song
    playlist_id = Column(Integer)  # FK to Playlist (null if single song)
    format = Column(String)  # mp3, m4a, etc.
    output_path = Column(String)
    downloaded_at = Column(DateTime(timezone=True), default=utc_now)