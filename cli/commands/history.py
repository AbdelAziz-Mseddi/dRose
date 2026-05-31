import typer
from rich.console import Console

from db.database import get_db_session
from db.models import Song
from db.repository import DownloadRecordRepository, PlaylistRepository


app = typer.Typer(
	name="history",
	help="i am here to show your download history, beware :p",
	no_args_is_help=True,
	add_completion=False,
)

console = Console()


@app.command()
def show(
	limit: int = typer.Option(10, "--limit", "-l", help="Number of recent downloads"),
):
	"""show recent download history"""
	session = get_db_session()
	try:
		repo = DownloadRecordRepository(session)
		records = repo.get_recent_downloads(limit=limit)

		if not records:
			console.print("[#FA5C5C]No downloads found yet.[/#FA5C5C]")
			raise typer.Exit()

		console.print("[#A8DF8E]Recent Downloads:[/#A8DF8E]")
		for idx, record in enumerate(records, start=1):
			song = session.query(Song).filter(Song.id == record.song_id).first()
			if song is None:
				title = "Unknown song"
				artist = "Unknown artist"
			else:
				title = song.title
				artist = song.artist or "Unknown artist"

			console.print(f"[#F0FFDF]{idx}. {title}[/#F0FFDF]")
			console.print(f"   [#6594B1]Artist:[/#6594B1] {artist}")
			console.print(f"   [#6594B1]Format:[/#6594B1] {record.format}")
			console.print(f"   [#6594B1]Output:[/#6594B1] {record.output_path}")
			console.print(f"   [#6594B1]Downloaded:[/#6594B1] {record.downloaded_at}")
	finally:
		session.close()


@app.command()
def delete():
	"""delete all download history permanently"""
	console.print("[#FA5C5C]This will permanently delete all download history.[/#FA5C5C]")
	if not typer.confirm("This is permanent. Continue?"):
		console.print("[#A8DF8E]Aborted.[/#A8DF8E]")
		raise typer.Exit()

	session = get_db_session()
	try:
		repo = DownloadRecordRepository(session)
		playlist_repo = PlaylistRepository(session)
		deleted_downloads = repo.delete_all_history()
		deleted_playlists = playlist_repo.delete_all_playlists()
		deleted_songs = session.query(Song).delete(synchronize_session=False)
		session.commit()
		console.print(
			f"[#A8DF8E]Deleted {deleted_downloads} downloads, {deleted_playlists} playlists, and {deleted_songs} songs.[/#A8DF8E]"
		)
	finally:
		session.close()


@app.command()
def playlists(
	downloaded: bool = typer.Option(
		False,
		"-d",
		"--downloaded",
		help="Show only playlists that have been downloaded",
	),
):
	"""show playlists from history"""
	session = get_db_session()
	try:
		repo = PlaylistRepository(session)
		items = repo.get_downloaded_playlists() if downloaded else repo.get_all_playlists()

		if not items:
			message = "No downloaded playlists found yet." if downloaded else "No playlists found yet."
			console.print(f"[#FA5C5C]{message}[/#FA5C5C]")
			raise typer.Exit()

		label = "Downloaded Playlists" if downloaded else "Playlists"
		console.print(f"[#A8DF8E]{label}:[/#A8DF8E]")
		for idx, playlist in enumerate(items, start=1):
			console.print(f"[#F0FFDF]{idx}. {playlist.name}[/#F0FFDF]")
			console.print(f"   [#6594B1]YouTube ID:[/#6594B1] {playlist.youtube_id}")
			console.print(f"   [#6594B1]URL:[/#6594B1] {playlist.youtube_url}")
	finally:
		session.close()
