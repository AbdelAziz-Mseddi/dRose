from . import downloader
from . import utils
from db.database import get_db_session
from db.repository import PlaylistRepository, DownloadRecordRepository, SongRepository
###

ydl_opts = {
    "extract_flat": True,  # Don't download videos, just get valid URLs/titles
    "dump_single_json": True,  # mimic the JSON output format
    "quiet": True,  # Suppress standard output
    "no_warnings": True,  # Suppress warnings
    "ignoreerrors": True,  # Skip private/deleted videos without stopping
}

import yt_dlp
###Retrieve playlist title, number of songs, and every song title###


def get_playlist_info(url):
    if not isinstance(url, str) or not url.strip():
        raise ValueError("Playlist URL is required.")
    url = utils.ensure_url_scheme(url)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            plInfo = ydl.extract_info(url, download=False)
    except Exception as exc:
        raise RuntimeError(
            "Could not fetch playlist details. Please check the URL and your internet connection."
        ) from exc

    if not isinstance(plInfo, dict):
        raise RuntimeError(
            "Could not fetch playlist details. The playlist may be private, deleted, or unavailable."
        )

    entries = plInfo.get("entries") or []
    res = {
        "duration": plInfo.get("duration"),
        "uploader": plInfo.get("uploader"),
        "title": plInfo.get("title"),
        "size": plInfo.get("playlist_count") or len(entries),
        "tracks": [
            (track.get("title"), track.get("duration"), track.get("uploader"))
            for track in entries
            if isinstance(track, dict)
        ],
    }
    return res


###Return a list of URLs for all songs in the playlist###


def get_song_urls_from_playlist(url):
    if not isinstance(url, str) or not url.strip():
        raise ValueError("Playlist URL is required.")
    url = utils.ensure_url_scheme(url)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            plInfo = ydl.extract_info(url, download=False)
    except Exception as exc:
        raise RuntimeError(
            "Could not fetch playlist tracks. Please check the URL and your internet connection."
        ) from exc

    if not isinstance(plInfo, dict):
        return []

    entries = plInfo.get("entries") or []
    if not entries:
        return []

    track_urls = []
    for track in entries:
        if not isinstance(track, dict):
            continue
        track_url = track.get("url")
        if not track_url:
            continue
        if isinstance(track_url, str) and track_url.startswith(("https://", "http://")):
            track_urls.append(track_url)
            continue
        video_id = track.get("id")
        if video_id:
            track_urls.append(f"https://music.youtube.com/watch?v={video_id}")
        else:
            track_urls.append(utils.ensure_url_scheme(str(track_url)))
    return track_urls


###Retrieve data for a single song (title, duration, etc.)###


def get_song_info(url):
    if not isinstance(url, str) or not url.strip():
        raise ValueError("Song URL is required.")
    url = utils.ensure_url_scheme(url)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            songInfo = ydl.extract_info(url, download=False)
    except Exception as exc:
        raise RuntimeError(
            "Could not fetch song details. Please check the URL and your internet connection."
        ) from exc

    if not isinstance(songInfo, dict):
        raise RuntimeError(
            "Could not fetch song details. The song may be private, deleted, or unavailable."
        )

    res = {
        "title": songInfo.get("title"),
        "duration": songInfo.get("duration"),
        "uploader": songInfo.get("uploader"),
        "view": songInfo.get("view_count"),
        "date": songInfo.get("upload_date"),
        "release": songInfo.get("release_date"),
        "artists": songInfo.get("artists"),
        "album": songInfo.get("album"),
    }
    return res


###DOWNLOAD PLAYLIST###


def download_playlist(url, output_folder=".", audio_format="mp3"):
    if not isinstance(output_folder, str) or not output_folder.strip():
        raise ValueError("Output folder path cannot be empty.")
    if not isinstance(audio_format, str) or not audio_format.strip():
        raise ValueError("Audio format cannot be empty.")

    url = utils.ensure_url_scheme(url)
    urls = get_song_urls_from_playlist(url)
    if not urls:
        raise ValueError(
            "No downloadable tracks found in this playlist. It may be empty, private, or unavailable."
        )

    downloaded_songs: int = 0
    failed_tracks: list[str] = []
    metadata = get_playlist_info(url)
    title = metadata.get("title") or "playlist"
    title = utils.sanitize_filename(title)
    utils.create_folder(title, output_folder)

    session = get_db_session()
    try:
        playlist_repo = PlaylistRepository(session)
        playlist = playlist_repo.get_or_create(
            name=metadata.get("title") or "playlist",
            youtube_id=metadata.get("id") or url,
            youtube_url=url,
        )
        session.commit()

        song_repo = SongRepository(session)
        record_repo = DownloadRecordRepository(session)

        for track in urls:
            try:
                adress, song_name = downloader.download_audio(
                    track,
                    f"{output_folder}/{title}",
                    audio_format,
                    playlist_id=playlist.id,
                )
                downloaded_songs += 1
            except Exception as exc:
                # Log the failure and continue with the next track
                failed_tracks.append(str(track))
                print(f"Warning: failed to download track {track}: {exc}")
                continue
    finally:
        session.close()
    return downloaded_songs


if __name__ == "__main__":
    get_playlist_info(
        "https://music.youtube.com/playlist?list=PLVe3Pb0zUL07V3hhdzjTsaiw7rp7Sg7eD&si=zY7y170jl-TAVuUy"
    )
    print(
        get_song_urls_from_playlist(
            "https://music.youtube.com/playlist?list=PLVe3Pb0zUL07V3hhdzjTsaiw7rp7Sg7eD&si=zY7y170jl-TAVuUy"
        )
    )
    print(
        get_song_info(
            "https://music.youtube.com/watch?v=4tJKyfXCDUE&si=aT8MPsNeI_7kDeWa"
        )
    )
    download_playlist(
        "https://music.youtube.com/playlist?list=PLVe3Pb0zUL04fRNvYJnpg5MFpzcoeT8qb&si=z51v5yyTOxzOZHVu"
    )
