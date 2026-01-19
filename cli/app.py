import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn
from cli.commands import config, doctor, playlist, song

console=Console()
#drose root command
app=typer.Typer(name="drose",
                no_args_is_help=False,
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
    logo = """
                                                                                                                                                                       
                                                                                                                                                                   
                                                                                           
                                                                                                                                                                   
                                                                                        .::: ++*#=     *%%%%@%                                         
                                                      ::--==:   -%@%=%%  :%@@@@= :@@@@+%@@@%:@@@@#     %@@@@@%                                         
                              #%%%@@%+  :@@@@@@@@=   .@@@@@@#  =@@@@@@@ .%@@@@@@-:@@@@+%@@@@:@@@@#     #@@@@@*                                         
                              @@%@@@@@% .@@@@@@@@@:  .@@@@@@#  @@@@@@@@ +@@@#%@@% -@@*  #@+  .%@*       #@*@@.                                         
                              @@@@@@@@@+.%@@%+*@@@=    @@%@#  :@@@. +@@.*@@.  @@%  @@+  *@+  .@@+       @%.@@*                                         
                                %@@. =@@# .@@#  %@@-   =@+#@@. -@@%     :+++:. *-+=-:%+  *@+   %@* .=-  +@*-@@%                                         
                                %@@. .@@#  @@@%@@@.    @@ -@@* -@@% -@@@++=:--+===-=-=---=:*  .@@# +@%  %@+-+@@:                                        
                               %@@.  @@#  @@%=#@@+   :@@@@@@% :@@%  .@@.+=-.:==-:+:--==+-=-=:.%@# +@@ =@%: +@@@+                                       
                               %@@. :@@%  @@% :@@@   =@*..+@@::@@@%+%@@ =::.:==:-*:.-:=-:===:=-@@@@@@-@@@@ @@@@#                                       
                               %@@=-%@@* *@@@+:@@@%=#@@@=+@@@@=#@@@@@@@ :+===-: .+:::::::.:=-=:-#@@@%-@@@@.@@@@#                                       
                              %@@@@@@@@: @@@@%.@@@@+%@@@++@@@%-.+===--=. +===-.-:+*-=-:---===:+-:                                                      
                              %@@@@@@@.  @@@@% =%@%=*%##-:*+=-:+=---==-=.+==- :-=-+=-===:..-:-+=-:++*#%#@@#                                            
                                              .            .-+#-=+=--.:.====: -+==:=.---:..-+=:-=-::+%@@@@%                                            
                                 -+*%@@@@@@@@@@%:        **@@@@@=+++=-=:+=-=- -===:+::-+++-+::==-.--=+=*@@%                                            
                                 @@@@@@@@@@@@@@@@@.     @@-+=#@@@--=+-:::+===- -===-.=---..-==+-.::-+++-+@%                                            
                                 @@@@@@@@@@@@@@@@@%    +@++-:+=@@@@*:::. =+--=-:.:-:-==..::-=-:---=+=.=@@@@                                            
                                 %@@@@@@@@@@@@@@@@@.   %@=+-::--@@@@@@. .--=====:--::::--===:%@*==.   =@@@@                                            
                                 :-%@@@@@   :%@%@@@:   %@=+-:.=..@@@@%..  ::. ..=-===-=-==+: @@@@@-    ::.                                             
                                   #@@@@@     @@@@%    %@%--:.::.%@#=%-.:==:#@--:-====++=.::==%@@@@@@@@-                                               
                                   *@@@@@   .%@@@%.    %@@@#..::-==+==-::-====:-%@*-+#@=----:+-@@@%+=-:                                                
                                   =@@@@@@@@@@@*       #=-==:::  %%::%=.-...::==  *@@=@@==+=--=#@@+   .@@@@*                                           
                                   =@@@@@++%@@@@@#     :+-+@::::   .:-@#:====+=++: :@@@@@*   -**@@#   .@@@@=                                           
                                   -@@@@%   .@@@@@- #-==-%#  -#@%-    : ..  =#@@:  *@@@@@%   :@@@@%.:-+@@@@=                                           
                                   -@@@@%   .@@@@@= *:++@@#.+        .::.:-=+=%@@@@@@@@@@* :@@@@@@@@@@@@@@@+                                           
                                   =@@@@@=- .%@@@@@@+=:*@@#.+        -:-:::-=+-@@@@@@@@@@: -@@@@@@@@@@@@@@@#                                           
                                 =@@@@@@@@@. #@@@@@@+=:-@@#.=   .+*#@-=====-:==-@@@@@@@@=  =@@@@@@@@@@@@@@@%                                           
                                 =@@@@@@@@@. +@@@@@@%-=::@%.= @@@@@@%.:++====-+:=%@@@%+  . .==-----:.                                                  
                                 *@@@@@@@@@.  #@@@@@%.=-   .= @@@%+ .--.:==++++-                :                                                      
                                 -%%%#+++=-         :: -+- .= ..:------::  :.                                                                          
                                        : ...... .:.--.   :==-==+-      .:                     .                                                       
                                         . ....:: --::---   =  =..= .             .   .       :                                                        
                                          . ::::--::--:::.. =               ..               .                                                         
                                           . :--:---.:::... =          .:::::.              .                                                          
                                            . .--::--:....  =     .::----:......           .                                                           
                                              . .--. -+*=:  -     .::::----::......      .                                                             
                                               .   +#:            .::::::::::::.. .    ..                                                              
                                                  *=              .::------::.::...  .                                                                 
                                                  =            .........:----:::  ..                                                                   
                                                  .               .:------.    :.                                                                      
                                                             ...       ..:.                                                                                                                                                                                                                                                                                                                                                                   
    """
    console.print(f"[#FFA240]{logo}[/#FFA240]")
    typer.echo(typer.style("Quick start:", fg=typer.colors.GREEN, bold=True))
    typer.echo("  drose --help     Show all commands")
    typer.echo("  drose [command]  Run a specific command")
    typer.echo()

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context ,
    version: bool = typer.Option(False, "--version", help="Show version"),
    help: bool = typer.Option(False, "--help", help="Show help", is_eager=True),
):
    """
    drose - Your CLI tool description
    """
    # Only show welcome if no command and no help/version flags
    if ctx.invoked_subcommand is None and not version and not help:
        print_welcome()
    
    if version:
        typer.echo("drose v0.1.0")


#initial commands
@app.command()
def version():
    """show version"""
    console.print("[red]DROSE v0.1.0[/red]")

@app.command()
def test():
    """testing command"""
    console.print("[violet]wiiiiiw[/violet]")

if __name__ == "__main__":
    app()