import typer
app=typer.Typer(
    name="config",
    help="i am in charge of your default configuration :p",
    no_args_is_help=True,
    add_completion=False
)


@app.command()
def set():
    """set default configuration"""
    pass

@app.command()
def get():
    """get the default configuration of a setting"""
    pass

@app.command()
def show():
    """show your full default configuration"""
    pass