import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn
from cli.commands import config, doctor, playlist

console=Console()
#drose root command
app=typer.Typer(name="drose",
                help="[#8A244B]drose[/#8A244B], [#5B23FF]your music companion :3[/#5B23FF]",
                no_args_is_help=True,
                add_completion=False)

#adding the precious commands
app.add_typer(config.app, name="config", help="Manage Configurations")
app.add_typer(doctor.app, name="doctor", help="Check System Requirements")
app.add_typer(playlist.app, name="playlist", help="Download and Manage Playlists")

main=app

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
    main()