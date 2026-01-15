import typer
import core.playlist as down
from rich.console import Console
app=typer.Typer(
    name="playlist",
    help="i am the main character, THE PLAYLIST BOSS :p",
    no_args_is_help=True,
    add_completion=False
)
console=Console()

@app.command()
def download(url : str = typer.Argument(..., help="lien URL de la playlist visée")):
    """download your favorite playlist"""
    console.print("[bold green]Starting download...🌹[/bold green]")
    console.print(f"URL: {url}")
    down.download_playlist(url)
    console.print("[bold green]🌹 Download complete![/bold green]")