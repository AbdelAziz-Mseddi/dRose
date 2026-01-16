import typer
import core.playlist as down
import core.utils as util
from rich.console import Console
from pathlib import Path
app=typer.Typer(
    name="playlist",
    help="i am the main character, THE PLAYLIST BOSS :p",
    no_args_is_help=True,
    add_completion=False
)
console=Console()

@app.command()
def download(url : str = typer.Argument(..., help="URL link of the Wanted Playlist"),
             output_dir : Path = typer.Option(Path("."), "--output_dir", "-o", help="Output Folder (Default: Current Directory)"),
             audio_format : str = typer.Option("mp3", "--format", "-f", help="Audio Format (Default: MP3)")
             ):
    """download your favorite playlist"""
    console.print("[bold green]Starting download...🌹[/bold green]")
    console.print(f"URL: {url}")
    down.download_playlist(url, output_dir, audio_format)
    console.print("[bold green]🌹 Download complete![/bold green]")

@app.command()
def point_info(url : str = typer.Argument(..., help="lien URL de la playlist visée")):
    """informations of the playlist"""
    box=down.get_playlist_info(url)
    console.print("[#213C51]Point Info on your beloved Playlist🌹[/#213C51]")
    console.print("[#6594B1]ø Playlist Title: [/#6594B1]", box["title"])
    console.print("[#6594B1]ø Uploader Username: [/#6594B1]", box["uploader"])
    console.print("[#6594B1]ø Number of Tracks: [/#6594B1]", box["size"])
    console.print("[#6594B1]ø Track List: [/#6594B1]")
    for track in box["tracks"]:
        console.print(f"  [#DDAED3]╠ {track[0]} [#B0FFFA]・゜゜・．[#B0FFFA]{util.format_duration(track[1])} [/#DDAED3]")
    console.print("🌹")