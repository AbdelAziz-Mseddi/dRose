import typer
app=typer.Typer(
    name="doctor",
    help="i am here to check your device's compatibility for Top-Tier Music :p",
    no_args_is_help=True,
    add_completion=False
)

@app.command()
def check():
    """check system requirements"""
    pass