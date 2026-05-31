from sqlalchemy.orm import Session
from db.models import Song, Playlist, DownloadRecord


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

    def delete_all_history(self):
        """Delete all download history rows"""
        count = self.session.query(DownloadRecord).delete(synchronize_session=False)
        return count


class PlaylistRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_or_create(
        self,
        name: str,
        youtube_id: str,
        youtube_url: str,
    ):
        """Get existing playlist or create new one"""
        playlist = (
            self.session.query(Playlist)
            .filter(Playlist.youtube_id == youtube_id)
            .first()
        )

        if not playlist:
            playlist = Playlist(
                name=name,
                youtube_id=youtube_id,
                youtube_url=youtube_url,
            )
            self.session.add(playlist)

        return playlist

    def get_all_playlists(self):
        """Get all stored playlists"""
        return self.session.query(Playlist).order_by(Playlist.created_at.desc()).all()

    def get_downloaded_playlists(self):
        """Get only playlists that have download history"""
        return (
            self.session.query(Playlist)
            .join(DownloadRecord, DownloadRecord.playlist_id == Playlist.id)
            .distinct()
            .order_by(Playlist.created_at.desc())
            .all()
        )

    def delete_all_playlists(self):
        """Delete all stored playlists"""
        count = self.session.query(Playlist).delete(synchronize_session=False)
        return count
