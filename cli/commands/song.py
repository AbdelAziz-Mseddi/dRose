import typer
import core.downloader as down
import core.playlist as infor
import core.utils as util
from cli import config_store as conf
from rich.console import Console
from pathlib import Path

app=typer.Typer(
    name="song",
    help="i am the main character's cousin, i.am.batman :p",
    no_args_is_help=True,
    add_completion=False
)
console=Console()

@app.command()
def download(url : str = typer.Argument(..., help="URL link of the Wanted Playlist(type between \"url\")"),
             output_dir : Path | None = typer.Option(None, "--output_dir", "-o", help="Output folder; defaults from config"),
             audio_format : str | None = typer.Option(None, "--format", "-f", help="Audio format; defaults from config")
             ):
    """download your favorite song"""
    console.print("[bold green]Starting download...🌹[/bold green]")
    console.print(f"URL: {url}")
    cfg = conf.get_config()
    eff_output = str(output_dir) if output_dir is not None else cfg.get("output_folder", ".")
    eff_format = audio_format if audio_format is not None else cfg.get("audio_format", "mp3")
    adress,name=down.download_audio(url, eff_output, eff_format)
    console.print("[#F6F0D7]🌹 Download complete![/#F6F0D7]")
    console.print("[#C5D89D] 🌹 File Name: [/#C5D89D]", name)
    console.print("[#9CAB84]  🌹 Location : [/#9CAB84]", adress)
    console.print("[#89986D]   🌹 See you around, Officer (^_~)[/#89986D]")

@app.command()
def point_info(url : str = typer.Argument(..., help="URL link of the Wanted Playlist"),
               all: bool = typer.Option(False, "--all", "-a", help="show duration, estimated size of playlist and songs, song artist")):
    """informations of the playlist"""
    box=infor.get_song_info(url)
    console.print("[#B8DB80]Point Info on your beloved Song🌹[/#B8DB80]")
    console.print("[#F7F6D3]ø Song Title: [/#F7F6D3]", box["title"])
    artist=box["uploader"]
    if (artist.endswith("- Topic")):
        artist=artist.replace("- Topic", "").rstrip()
    console.print("[#F7F6D3]ø Uploader Username: [/#F7F6D3]", artist)
    console.print("[#F7F6D3]ø Song Duration: [/#F7F6D3]", util.format_duration(box["duration"]))
    if (all):
        console.print("[#FFE4EF]ø Release Date: [/#FFE4EF]", util.format_date(box["date"]))
        console.print("[#FFE4EF]ø Estimated Size: [/#FFE4EF]", util.format_size(box["duration"]*192//8))
    console.print("[#F39EB6]🌹 See you, Space Cowboy...[/#F39EB6]")