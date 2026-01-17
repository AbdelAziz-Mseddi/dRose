import typer
import core.playlist as down
import core.utils as util
from cli import config_store as conf
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
def download(url : str = typer.Argument(..., help="URL link of the Wanted Playlist(type between \"url\")"),
             output_dir : Path | None = typer.Option(None, "--output_dir", "-o", help="Output folder; defaults from config"),
             audio_format : str | None = typer.Option(None, "--format", "-f", help="Audio format; defaults from config")
             ):
    """download your favorite playlist"""
    console.print("[bold green]Starting download...🌹[/bold green]")
    console.print(f"URL: {url}")
    cfg = conf.get_config()
    eff_output = str(output_dir) if output_dir is not None else cfg.get("output_folder", ".")
    eff_format = audio_format if audio_format is not None else cfg.get("audio_format", "mp3")
    down.download_playlist(url, eff_output, eff_format)
    console.print("[bold green]🌹 Download complete![/bold green]")

@app.command()
def point_info(url : str = typer.Argument(..., help="URL link of the Wanted Playlist"),
               all: bool = typer.Option(False, "--all", "-a", help="show duration, estimated size of playlist and songs, song artist")):
    """informations of the playlist"""
    box=down.get_playlist_info(url)
    console.print("[#213C51]Point Info on your beloved Playlist🌹[/#213C51]")
    console.print("[#6594B1]ø Playlist Title: [/#6594B1]", box["title"])
    console.print("[#6594B1]ø Uploader Username: [/#6594B1]", box["uploader"])
    console.print("[#6594B1]ø Number of Tracks: [/#6594B1]", box["size"])
    console.print("[#6594B1]ø Track List: [/#6594B1]")
    totDur=0
    for track in box["tracks"]:
        if(all):
            console.print(f"  [#DDAED3]╠ {track[0]}[/#DDAED3], [#FFDAB3]{track[2]}[/#FFDAB3][#B0FFFA]・゜゜・．{util.format_duration(track[1])}[/#B0FFFA] [#F5FBE6] ◁◁ ▐ ▌ ▷▷ {util.format_size(track[1]*192//8)}[/#F5FBE6]")
        else:
            console.print(f"  [#DDAED3]╠ {track[0]} [/#DDAED3]")
        totDur+=track[1]
    if(not all):
        console.print("🌹")
    else:
        console.print("🌹 Total Duration: ",util.format_duration(totDur), "ø Estimated Total Size: ", util.format_size(totDur*192//8))