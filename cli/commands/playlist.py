import typer
import core.playlist as down
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
def download(url : str = typer.Argument(..., help="lien URL de la playlist visée"),
             output_dir : Path = typer.Option(Path("."), "--output_dir", "-o", help="Output Folder (Default: Current Directory)"),
             audio_format : str = typer.Option("mp3", "--format", "-f", help="Audio Format (Default: MP3)")
             ):
    """download your favorite playlist"""
    console.print("[bold green]Starting download...🌹[/bold green]")
    console.print(f"URL: {url}")
    down.download_playlist(url, output_dir, audio_format)
    console.print("[bold green]🌹 Download complete![/bold green]")