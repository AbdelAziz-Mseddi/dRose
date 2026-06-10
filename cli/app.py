import typer
from rich.console import Console
from rich.prompt import Prompt
from cli.commands import config, doctor, history
from core.utils import (
    zip_folder,
    format_duration,
    format_size,
    format_date,
    spinner2016,
    spinner2017,
    spinner2018,
    is_song_url,
    sanitize_filename,
    create_folder,
)
from core.playlist import (
    download_playlist,
    get_playlist_info,
    get_song_info,
    get_song_urls_from_playlist,
)
from core.downloader import download_audio
from cli import config_store as defConf
from pathlib import Path
from cli import config_store as conf
import re
from pyfiglet import Figlet
import ascii_magic
import shutil
import sys
import io

console = Console()
# drose root command
app = typer.Typer(
    name="drose",
    no_args_is_help=False,
    add_completion=False,
    help="[#8A244B]drose[/#8A244B], [#5B23FF]your music companion :3[/#5B23FF]",
)

# adding the precious commands
app.add_typer(config.app, name="config", help="Manage Configurations")
app.add_typer(doctor.app, name="doctor", help="Check System Requirements")
app.add_typer(history.app, name="history", help="Show download history")


def print_welcome():

    asset_dir = Path(__file__).resolve().parents[1] / "assets"
    img_path = asset_dir / "dRose.png"

    try:
        art = ascii_magic.AsciiArt.from_image(str(img_path))
        # for a more scalable output when terminal is reduced
        term_cols = shutil.get_terminal_size((120, 24)).columns
        # to capture to_terminal output and manipulate it
        buffer = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buffer
        # printing to sys.stdout (what we will capture)
        art.to_terminal(columns=min(100, term_cols), char="@%#*+=-:. "[::-1])
        # restoring the normal sys.stdout (to print to the terminal again)
        sys.stdout = sys_stdout
        # getting the captured output
        ascii_text = buffer.getvalue()
        # getting the lines seperated so we can crop the output
        lines = ascii_text.split("\n")
        nbre_lines = len(lines)
        minn = int(nbre_lines * 0.25)
        maxx = int(nbre_lines * 0.8)
        cropped = "\n".join(lines[minn:maxx:])
        print(cropped)
    except Exception:
        # If ascii-magic (or its image deps) can't render, fall back to a bundled text banner.
        for filename in ("drose-ascii.txt", "drose-ascii-2.txt"):
            try:
                fig = Figlet(font="slant")
                logo = fig.renderText("""Dragoula
            Rose""")
                console.print(f"[#FFA240]{logo}[/#FFA240]")
                break
            except FileNotFoundError:
                continue

    typer.echo(typer.style("Quick start:", fg=typer.colors.BLUE, bold=True))
    typer.echo("  drose --help     Show all commands")
    typer.echo("  drose [command]  Run a specific command")
    typer.echo("  drose [squint] [your] [eyes] -:3")
    typer.echo()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "-v", "--version", help="Show version"),
):
    """
    drose :3
    """
    # Only show welcome if no command and no version flag
    if ctx.invoked_subcommand is None and not version:
        print_welcome()
    if version:
        typer.echo("drose v1.2.0")


# initial commands
# @app.command()
# def version():
#     """show version"""
#     console.print("[red]DROSE v0.1.0[/red]")

# @app.command()
# def test():
#     """testing command"""
#     console.print("[violet]wiiiiiw[/violet]")


# useful command
@app.command()
def zip(
    path: str = typer.Argument(..., help="Path to directory or file to zip"),
    output: str = typer.Option(
        None,
        "--output",
        "-o",
        help="Output zip file path (default=your_output_folder/name)",
    ),
):
    """Zipping your Playlist"""
    if output is None:
        conf = defConf.get_config()[0]
        zip_folder(path, f"{conf['output_folder']}/{Path(path).name}")
        console.print("[#9CAB84]Zipped successfully.[/#9CAB84]")
        console.print(
            f"[#9CAB84]🌹 Location : {conf['output_folder']}/{Path(path).name}[/#9CAB84]"
        )
    else:
        zip_folder(path, output)
        console.print("[#9CAB84]Zipped successfully.[/#9CAB84]")
        adress = Path(output).resolve()
        console.print(f"[#9CAB84]🌹 Location : {adress}[/#9CAB84]")


# THE commands
@app.command()
def playlist(
    url: str = typer.Argument(..., help="URL link of the Wanted Playlist"),
    output_dir: Path | None = typer.Option(
        None, "--output_dir", "-o", help="Output folder; defaults from config"
    ),
    audio_format: str | None = typer.Option(
        None, "--format", "-f", help="Audio format; defaults from config"
    ),
    alll: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Show Duration, Estimated Size of Playlist and Songs, Artists",
    ),
    listt: bool = typer.Option(False, "--list", "-l", help="List Songs + Informations"),
    prompt_each: bool = typer.Option(
        False, "--prompt", "-p", help="Prompt for each song before downloading"
    ),
):
    """Download and Manage Playlists"""
    try:
        is_song, _ = is_song_url(url)
    except Exception as exc:
        raise typer.BadParameter(str(exc)) from exc

    if is_song:
        console.print(
            "[#B8DB80]Looks like it's a song URL, not a playlist URL.[/#B8DB80]"
        )
        console.print("[#B8DB80]Hold your horse, i'm gonna bootleg it 🏎️[/#B8DB80]")
        song(
            urls=[url],
            alll=alll,
            listt=listt,
            output_dir=output_dir,
            audio_format=audio_format,
        )
        return

    if listt:
        what = "Playlist"
        with spinner2016("Fetching playlist details"):
            box = get_playlist_info(url)
        title = box["title"]
        artist = box["uploader"]
        preArtist = "Uploader Username: "
        if title.startswith("Album - "):
            what = "Album"
            title = title.replace("Album - ", "").lstrip()
            artist = []
            for zong in box["tracks"]:
                name = zong[2]
                if name is None:
                    name = Prompt.ask("We could not fetch this song's artist's name, who is he ?", default="Anonymous")
                elif name.endswith("- Topic"):
                    name = name.replace("- Topic", "").rstrip()
                if name not in artist:
                    artist.append(name)
            preArtist = (
                "Artist Name: " if len(artist) == 1 else "Artists Collaborating: "
            )
            if preArtist == "Artists Collaborating: ":
                artist = ", ".join(artist)
            else:
                artist = artist[0]
        console.print(f"[#B8DB80]Point Info on your beloved {what} 🌹[/#B8DB80]")
        console.print(f"[#6594B1]ø {what} Title: [/#6594B1]", title)
        console.print(f"[#6594B1]ø {preArtist}[/#6594B1]", artist)
        console.print("[#6594B1]ø Number of Tracks: [/#6594B1]", box["size"])
        console.print("[#6594B1]ø Track List: [/#6594B1]")
        totDur = 0
        for track in box["tracks"]:
            if track[0] != "[Deleted video]":
                if alll:
                    artist = track[2]
                    if name is None:
                        name = Prompt.ask("We could not fetch this song's artist's name, who is he ?", default="Anonymous")
                    elif artist.endswith("- Topic"):
                        artist = artist.replace("- Topic", "").rstrip()
                    console.print(
                        f"  [#DDAED3]╠ {track[0]}[/#DDAED3], [#FFDAB3]{artist}[/#FFDAB3][#B0FFFA]・゜゜・．{format_duration(track[1])}[/#B0FFFA] [#F5FBE6] ◁◁ ▐ ▌ ▷▷ {format_size(track[1] * 192000 // 8)}[/#F5FBE6]"
                    )
                else:
                    console.print(f"  [#DDAED3]╠ {track[0]} [/#DDAED3]")
                totDur += track[1]
        if not alll:
            console.print("🌹")
        else:
            console.print(
                "🌹 Total Duration: ",
                format_duration(totDur),
                " ø Estimated Total Size: ",
                format_size(totDur * 192000 // 8),
            )
    else:
        downloaded_songs : int = 0
        console.print(f"URL: {url}")
        cfg = conf.get_config()
        eff_output = (
            str(output_dir)
            if output_dir is not None
            else cfg[0].get("output_folder", ".")
        )
        eff_format = (
            audio_format
            if audio_format is not None
            else cfg[0].get("audio_format", "mp3")
        )
        if prompt_each:
            console.print("[#cdb4db]Starting interactive download...🌹[/#cdb4db]")
            with spinner2018("Making a tour around the playlist"):
                metadata = get_playlist_info(url)
                urls = get_song_urls_from_playlist(url)

            pl_title = metadata.get("title") or "playlist"
            safe_title = sanitize_filename(pl_title)
            create_folder(safe_title, eff_output)

            for idx, track_url in enumerate(urls, start=1):
                console.print(f"[#ffc8dd]Song {idx}/{len(urls)}[/#ffc8dd]")
                try:
                    with spinner2018("Fetching song details"):
                        info = get_song_info(track_url)
                except Exception:
                    console.print("[red]Could not fetch song details; skipping.[/red]")
                    continue
                title = info.get("title") or track_url
                duration = info.get("duration") or 0
                console.print(
                    f"  [#ffafcc]{title}[/#ffafcc] — {format_duration(duration)} — {format_size(duration * 192000 // 8)}"
                )
                if typer.confirm(f"Download '{title}'?"):
                    console.print("Downloading...")
                    try:
                        adress, name = download_audio(track_url, f"{eff_output}/{safe_title}", eff_format)
                        downloaded_songs += 1
                        console.print("[#bde0fe]🌹 Download complete![/#bde0fe]")
                    except Exception:
                        console.print("[red]Failed to download track :([/red]")

            console.print(f"[#a2d2ff]Downloaded {downloaded_songs} songs 🌹[/#a2d2ff]")
        else:
            console.print("[#FF5C00]Starting download...🌹[/#FF5C00]")
            with spinner2017("We are cooking"):
                downloaded_songs = download_playlist(url, eff_output, eff_format)
            console.print(f"[bold green]Downloaded {downloaded_songs} songs 🌹[/bold green]")


@app.command()
def song(
    urls: list[str] = typer.Argument(..., help="One or more URL links of wanted songs"),
    alll: bool = typer.Option(
        False, "--all", "-a", help="Show additional Info (Release Date, Estimated Size)"
    ),
    listt: bool = typer.Option(
        False, "--list", "-l", help="Show song Information without Downloading"
    ),
    output_dir: Path | None = typer.Option(
        None, "--output_dir", "-o", help="Output folder; defaults from config"
    ),
    audio_format: str | None = typer.Option(
        None, "--format", "-f", help="Audio format; defaults from config"
    ),
):
    """Download and Manage Songs"""
    cfg = conf.get_config()
    eff_output = (
        str(output_dir) if output_dir is not None else cfg[0].get("output_folder", ".")
    )
    eff_format = (
        audio_format if audio_format is not None else cfg[0].get("audio_format", "mp3")
    )

    for idx, url in enumerate(urls, start=1):
        if len(urls) > 1:
            console.print(f"[#B8DB80]Song {idx}/{len(urls)}[/#B8DB80]")

        try:
            is_song, _ = is_song_url(url)
        except Exception as exc:
            raise typer.BadParameter(str(exc)) from exc

        if not is_song:
            console.print(
                "[#B8DB80]Looks like it's a playlist URL, not a song URL.[/#B8DB80]"
            )
            console.print("[#B8DB80]Hold your horse, i'm gonna bootleg it 🏎️[/#B8DB80]")
            playlist(
                url=url,
                output_dir=output_dir,
                audio_format=audio_format,
                alll=alll,
                listt=listt,
            )
            continue

        if listt:
            console.print("[#B8DB80]Point Info on your beloved Song 🌹[/#B8DB80]")
            with spinner2017("Fetching song details"):
                box = get_song_info(url)
            album = box.get("album")
            artists = box.get("artists")
            if isinstance(artists, str):
                artist_list = re.split(
                    r",|&|feat\.?|ft\.?", artists, flags=re.IGNORECASE
                )
                artists = [a.strip() for a in artist_list if a.strip()]
            mul_art = True if artists is not None and len(artists) > 1 else False
            artist = ", ".join(artists) if artists is not None else box["uploader"]
            console.print("[#F7F6D3]ø Song Title: [/#F7F6D3]", box["title"])
            if mul_art:
                preartist = "ø Artists collaborating: "
            elif box.get("artists") is not None:
                preartist = "ø Artist: "
            else:
                preartist = "ø Uploader Username: "
            if artist is None:
                artist = input()
            elif artist.endswith("- Topic"):
                artist = artist.replace("- Topic", "").rstrip()
            console.print(f"[#F7F6D3]{preartist}[/#F7F6D3]", artist)
            console.print(
                "[#F7F6D3]ø Song Duration: [/#F7F6D3]",
                format_duration(box["duration"]),
            )
            if album is not None:
                console.print("[#F7F6D3]ø Album: [/#F7F6D3]", album)
            if alll:
                release = box.get("release")
                release = box.get("date") if release is None else release
                console.print(
                    "[#FFE4EF]ø Release Date: [/#FFE4EF]", format_date(release)
                )
                console.print(
                    "[#FFE4EF]ø Estimated Size: [/#FFE4EF]",
                    format_size(box["duration"] * 192000 // 8),
                )
            console.print("[#F39EB6]🌹 See you, Space Cowboy...[/#F39EB6]")
            continue

        console.print("[bold green]Starting download...🌹[/bold green]")
        console.print(f"URL: {url}")
        adress, name = download_audio(url, eff_output, eff_format)
        console.print("[#F6F0D7]🌹 Download complete![/#F6F0D7]")
        console.print("[#C5D89D] 🌹 File Name: [/#C5D89D]", name)
        if idx == len(urls):
            console.print("[#9CAB84]  🌹 Location : [/#9CAB84]", adress)
            console.print("[#89986D]   🌹 See you around, Officer (^_~)[/#89986D]")


if __name__ == "__main__":
    app()
