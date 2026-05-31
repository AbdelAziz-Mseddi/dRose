from sqlalchemy.orm import Session
from db.models import Song, DownloadRecord


class SongRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_or_create(
        self,
        title: str,
        artist: str,
        duration: float,
        youtube_id: str,
        youtube_url: str,
    ):
        """Get existing song or create new one"""
        song = self.session.query(Song).filter(Song.youtube_id == youtube_id).first()

        if not song:
            song = Song(
                title=title,
                artist=artist,
                duration=duration,
                youtube_id=youtube_id,
                youtube_url=youtube_url,
            )
            self.session.add(song)
        # we will leave commiting and flushing to be external to repository utils
        return song


class DownloadRecordRepository:
    def __init__(self, session: Session):
        self.session = session

    def log_download(
        self, song_id: int, format: str, output_path: str, playlist_id: int = None
    ):
        """Log a download"""
        record = DownloadRecord(
            song_id=song_id,
            playlist_id=playlist_id,
            format=format,
            output_path=output_path,
        )
        self.session.add(record)
        # we will leave commiting and flushing to be external to repository utils
        return record

    def get_all_downloads(self):
        """Get all download history"""
        return self.session.query(DownloadRecord).all()

    def get_recent_downloads(self, limit: int = 10):
        """Get most recent downloads"""
        return (
            self.session.query(DownloadRecord)
            .order_by(DownloadRecord.downloaded_at.desc())
            .limit(limit)
            .all()
        )
