import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn
from cli.commands import config, doctor, playlist

console=Console()
#drose root command
app=typer.Typer(name="drose",
                help="i am dragoula, your sense of Music's savior:3",
                no_args_is_help=True,
                add_completion=False)
app.add_typer(config.app, name="config", help="Manage Configurations")
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