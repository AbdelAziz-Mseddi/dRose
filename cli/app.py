import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn

app=typer.Typer(name="drose",
                help="i am homelander, your savior:)",
                no_args_is_help=True,
                add_completion=False)
console=Console()

main=app

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