import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn
from cli.commands import config, doctor, playlist, song
from core.utils import zip_folder
from cli import config_store as defConf
from pathlib import Path

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
app.add_typer(playlist.app, name="playlist", help="Download and Manage Playlists")
app.add_typer(song.app, name="song", help="Download and Manage Songs")


console=Console()
def print_welcome():
    """Your personalized welcome message"""
    logo = """          .                                                                                .    .   
                  .                                 .                 .        .                    
                    .                 .    .                                             .       .  
         .. .      .     .                  .       .                                    .          
                              .                  .               .                                  
                                                     :=. .=+:*#=*@@:  -@@@%              ..         
    .                  . .++**- +@@@@+  +@@@* *@@@@:%@@@*+@@+@@#%@@-  -@@@%                         
                         :@@@@@=#@@@@@- =@@@+.@@#@@=@@=@@.%@.+%. @*    @#@=                    .    
       .     .            +@:-@#.%#.*@: -@*@=-@@  .-*+:=+=+*:=%. @#:*:-@%@@       .     .           
               .      .   =@::@% %@@@+  *@%@#-@@:%@+=:-=-=-==--:.@#=@=*@.*@=                        
                          =@:-@%.@%.@@-:@#-@@+@@@@@:=---:*:---==-*@@@#@@*@@@.        .         .    
   .                     .@@@@@=*@@+@@@#@@+@@*=#*+*:===::*=---=-==-::..:....      .      .          
                  .      .@@%#- -++:.-:... ..:++--====:-=-==---:=+=#@@@@@:              .           
                         . :##@@@@@@%=   .*#@@@+++=-==--======---=--==*%@.                     .    
    .                      =@@@@@@@@@@+  *%+=#@@#==-===-:---=::=+--+*=%@@:                         .
      .  .    .            -@@@@@@@@@@@ .%#+-=:@@@*:=----==--===+@@*  #@@:         .              . 
         ..           .  .   @@@+  #@@* .%@+--:*%#*-==++=+====-=*@@@@@%   .    .                    
                             @@@@%@@@=. .+#*+-:=+=+--:=+-#@*@+++=*@@. -**:        .      .          
                             @@@#-%@@@: .=+@=:::==+--+**=.-@@@*..#@@  *@@=    .                     
     ..                   .  @@@+ :@@@-*=*@+=:    --=+*@@@@@@@++@@@@@@@@@=           .       .      
         .                 .%@@@@#:@@@@%=#@+-   .-++=-++@@@@@@:*@@@@@@@@@+      .                   
                           :@@@@@%.@@@@@=-@+-%@@@*-**+++-@@@+  :=---:.                              
             .             :@@@%%*..=**-:=-.:-=-----::::.  .   .  .                                 
        .                    .  ...:::---:..::==::::.      .  .                                     
              ..        .        .:-:-----:.:         ..        ..                        .         
                         .        .:----::..:   .:---::...     .                           .        
                                   ..::-*=. .   :-----:::..   .                           .         
 .            .                       *.       .:------::...:                      ..          .    
                                  .  ..        .:-----::...                 .                       
             .                .              .........                      .                    . .
                                 .                                 .   .                   .        
     .                           .                                                 .        .       
                                .                   .                                               
     . .                         .                                                .                 
                                                                          .                         """
    console.print(f"[#FFA240]{logo}[/#FFA240]")
    typer.echo(typer.style("Quick start:", fg=typer.colors.BLUE, bold=True))
    typer.echo("  drose --help     Show all commands")
    typer.echo("  drose [command]  Run a specific command")
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
    """zipping your playlist"""
    if output is None:
        conf=defConf.get_config()[0]
        zip_folder(path, f"{conf["output_folder"]}/{Path(path).name}")
    else:
        zip_folder(path, output)

if __name__ == "__main__":
    app()