import typer
from rich.console import Console
from cli.commands import config, doctor
from core.utils import zip_folder,format_duration, format_size, format_date, spinner2016, spinner2017
from core.playlist import download_playlist, get_playlist_info, get_song_info, get_song_urls_from_playlist
from core.downloader import download_audio
from cli import config_store as defConf
from pathlib import Path
from cli import config_store as conf


console=Console()
#drose root command
app=typer.Typer(name="drose",
                no_args_is_help=False,
                add_completion=False,
                help="[#8A244B]drose[/#8A244B], [#5B23FF]your music companion :3[/#5B23FF]",
                )

#adding the precious commands
app.add_typer(config.app, name="config", help="Manage Configurations")
app.add_typer(doctor.app, name="doctor", help="Check System Requirements")

console=Console()
def print_welcome():
    """Your personalized welcome message"""
    logo = """                                        .                   .   .                                                                  
  .                   .                         .                 .           .                         
                                                                      .      .  
                                                                                                           
                               .           .        :=*.%@@@.   -@@@@@                                 
              .-=***.    @@@@@:  @@@@@@ +@@@@@ @@@@-@@@+@@@@:   -@@@@@                   .             
     .@@@@@@@ @@@@@@@@.  @@@@@- @@@@@@@ @@@@@@#@@@@:@@@-*@@@     #@@@.               . .               
     .@@@@@@@+@@@@@@@@   #@@@@  @@@.%@@-@@. @@@ @@+ *@+  @@=     @@@@@                                 
      .@@  @@@ @@@ +@@   %@.@@  @@#    ###= @:-::@+ +@+  @@* #+ :@@#@@   .                   ..        
       @@  @@@ @@@@@@    @@ @@= @@# @@@##-*:::::::::::=  @@*-@@ @@:.@@+                                
       @@  @@@ @@@ @@@   @@%@@@.@@@:+@@##+-::::::-:::::::#@@@@@@@@@=@@@+         .                     
       @@..@@@ @@@ @@@@:@@@ @@@@@@@@@@@.-::::::*:::::::=::#@@@@%@@@=@@@*               .     .         
      @@@@@@@.@@@@@@@@@=@@@ @@@@ @*##*+ ::::.::=::::::::::::                                           
      @@@@@@  %@@@# @@@ =:.     ###:*##=::::::::+::::::::#::@@@@@@@@                                   
            .   .--         *@@@@####+=::::::-:::::::=+=:::::##*@@@@                                   
        @@@@@@@@@@@@@@     @##@@@@=###-:=:::.::::::::::::::=.+*##*@@     .                          .  
        @@@@@@@@@@@@@@@   @@####@@@@=**-::::::::::::::::::=*###:@@@@                .             .    
        @@@@@@@@@@@@@@@   @%##:#=@@@@@..#:::::::::::::::@@@%*   @@@@       .                           
          @@@@%   @@@@@   @@#*+*: @@@@=: ##---:::::::::#%@@@@+*%*                                      
          @@@@% . @@@@.   @@@#+ -.@***###=*+%#@@:-*--=+*#%@@@@@@@                  .      .            
 .    .   @@@@@@@@@@=     @@###-: @#=@*+=:.### *@@*@####+#@@@   @@@@          .                        
          @@@@@*%@@@@@    ##@@ :.  -*+@+=######  @@@@@  :#@@@   @@@@                                   
          @@@@*  -@@@@ #@#-*@ @@=     -+##+@@@@@@@@@@@ *@@@@@@@@@@@@                 .   .             
          @@@@@  -@@@@*@*#@@@.       *=+=*##=@@@@@@@@% @@@@@@@@@@@@@                                   
        *@@@@@@@= @@@@@@#-@@@.     +@####*-##=@@@@@@@  @@@@@@@@@@@@@             .                     
        *@@@@@@@- @@@@@@-#:@@. @@@@@@.#######+#@@@@+   +*+++=-.           .       ..                   
        @@@@@@@@-  @@@@@ ##. . @@@- -==.-*#*##             .    .                                       
                                      .           .            .--:     -                                                          
                                                                                                  .                                
                                                                                  .                 .
                                                 .
    .          .                                                                     .       .        .
                                  .                                                                .          .                    
     .                                     .                                                                        .              
                                                                                                               .                   
                                   .                                   .                                      .                    
"""
    console.print(f"[#FFA240]{logo}[/#FFA240]")
    typer.echo(typer.style("Quick start:", fg=typer.colors.BLUE, bold=True))
    typer.echo("  drose --help     Show all commands")
    typer.echo("  drose [command]  Run a specific command")
    typer.echo("  drose [squint] [your] [eyes] -:3")
    typer.echo()

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="Show version"),
):
    """
    drose :3
    """
    # Only show welcome if no command and no version flag
    if ctx.invoked_subcommand is None and not version:
        print_welcome()
    if version:
        typer.echo("drose v0.1.0")


#initial commands
# @app.command()
# def version():
#     """show version"""
#     console.print("[red]DROSE v0.1.0[/red]")

# @app.command()
# def test():
#     """testing command"""
#     console.print("[violet]wiiiiiw[/violet]")

#useful command
@app.command()
def zip(
    path: str = typer.Argument(..., help="Path to directory or file to zip"),
    output: str = typer.Option(None, "--output", "-o", help="Output zip file path (default=your_output_folder/name)"),
):
    """Zipping your Playlist"""
    if output is None:
        conf=defConf.get_config()[0]
        zip_folder(path, f"{conf["output_folder"]}/{Path(path).name}")
        console.print("[#9CAB84]Zipped successfully.[/#9CAB84]")
        console.print(f"[#9CAB84]🌹 Location : {conf["output_folder"]}/{Path(path).name}[/#9CAB84]")
    else:
        zip_folder(path, output)

#THE commands
@app.command()
def playlist(
    url : str = typer.Argument(..., help="URL link of the Wanted Playlist"),
    output_dir : Path | None = typer.Option(None, "--output_dir", "-o", help="Output folder; defaults from config"),
    audio_format : str | None = typer.Option(None, "--format", "-f", help="Audio format; defaults from config"),
    alll : bool = typer.Option(False, "--all", "-a", help="Show Duration, Estimated Size of Playlist and Songs, Artists"),
    listt : bool = typer.Option(False, "--list", "-l", help="List Songs + Informations")
):
    """Download and Manage Playlists"""
    if(listt):
        what="Playlist"
        with spinner2016("Fetching playlist details"):
            box=get_playlist_info(url)
        title=box["title"]
        artist=box["uploader"]
        preArtist="Uploader Username: "
        if title.startswith("Album - ") :
            what="Album"
            console.print(f"[#B8DB80]Point Info on your beloved {what}🌹[/#B8DB80]")
            title=title.replace("Album - ", "").lstrip()
            artist=[]
            for zong in box["tracks"]:
                name=zong[2]
                if name not in artist:
                    artist.append(name)
            preArtist="Artist Name: " if len(artist)==1 else "Artists Collaborating: "
            if preArtist == "Artists Collaborating: " :
                artist=", ".join(artist)
            else :
                artist=artist[0]
        console.print(f"[#6594B1]ø {what} Title: [/#6594B1]", title)
        console.print(f"[#6594B1]ø {preArtist}[/#6594B1]", artist)
        console.print("[#6594B1]ø Number of Tracks: [/#6594B1]", box["size"])
        console.print("[#6594B1]ø Track List: [/#6594B1]")
        totDur=0
        for track in box["tracks"]:
            if( track[0]!='[Deleted video]'):
                if(alll):
                    artist=track[2]
                    if (artist.endswith("- Topic")):
                        artist=artist.replace("- Topic", "").rstrip()
                    console.print(f"  [#DDAED3]╠ {track[0]}[/#DDAED3], [#FFDAB3]{artist}[/#FFDAB3][#B0FFFA]・゜゜・．{format_duration(track[1])}[/#B0FFFA] [#F5FBE6] ◁◁ ▐ ▌ ▷▷ {format_size(track[1]*192000//8)}[/#F5FBE6]")
                else:
                    console.print(f"  [#DDAED3]╠ {track[0]} [/#DDAED3]")
                totDur+=track[1]
        if(not alll):
            console.print("🌹")
        else:
            console.print("🌹 Total Duration: ",format_duration(totDur), " ø Estimated Total Size: ", format_size(totDur*192000//8))
    else:
        console.print("[#FF5C00]Starting download...🌹[/#FF5C00]")
        console.print(f"URL: {url}")
        cfg = conf.get_config()
        eff_output = str(output_dir) if output_dir is not None else cfg[0].get("output_folder", ".")
        eff_format = audio_format if audio_format is not None else cfg[0].get("audio_format", "mp3")
        with spinner2017("We are cooking"):
            download_playlist(url, eff_output, eff_format)
        console.print("[bold green]🌹 Download complete![/bold green]")

@app.command()
def song(url : str = typer.Argument(..., help="URL link of the Wanted Song"),
    alll : bool = typer.Option(False, "--all", "-a", help="Show additional Info (Release Date, Estimated Size)"),
    listt : bool = typer.Option(False, "--list", "-l", help="Show song Information without Downloading"),
    output_dir : Path | None = typer.Option(None, "--output_dir", "-o", help="Output folder; defaults from config"),
    audio_format : str | None = typer.Option(None, "--format", "-f", help="Audio format; defaults from config")
):
    """Download and Manage Songs"""
    if(listt):
        console.print("[#B8DB80]Point Info on your beloved Song🌹[/#B8DB80]")
        with spinner2017("Fetching song details"):
            box=get_song_info(url)
        console.print("[#F7F6D3]ø Song Title: [/#F7F6D3]", box["title"])
        artist=box["uploader"]
        if (artist.endswith("- Topic")):
            artist=artist.replace("- Topic", "").rstrip()
        console.print("[#F7F6D3]ø Uploader Username: [/#F7F6D3]", artist)
        console.print("[#F7F6D3]ø Song Duration: [/#F7F6D3]", format_duration(box["duration"]))
        if (alll):
            console.print("[#FFE4EF]ø Release Date: [/#FFE4EF]", format_date(box["date"]))
            console.print("[#FFE4EF]ø Estimated Size: [/#FFE4EF]", format_size(box["duration"]*192000//8))
        console.print("[#F39EB6]🌹 See you, Space Cowboy...[/#F39EB6]")
    else:
        console.print("[bold green]Starting download...🌹[/bold green]")
        console.print(f"URL: {url}")
        cfg = conf.get_config()
        eff_output = str(output_dir) if output_dir is not None else cfg[0].get("output_folder", ".")
        eff_format = audio_format if audio_format is not None else cfg[0].get("audio_format", "mp3")
        adress,name=download_audio(url, eff_output, eff_format)
        console.print("[#F6F0D7]🌹 Download complete![/#F6F0D7]")
        console.print("[#C5D89D] 🌹 File Name: [/#C5D89D]", name)
        console.print("[#9CAB84]  🌹 Location : [/#9CAB84]", adress)
        console.print("[#89986D]   🌹 See you around, Officer (^_~)[/#89986D]")

if __name__ == "__main__":
    app()