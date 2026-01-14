import typer
import core.downloader
app=typer.Typer(
    name="playlist",
    help="i am the main character, THE PLAYLIST BOSS :p",
    no_args_is_help=True,
    add_completion=False
)

@app.command
def download():
    """download your favorite playlist"""
    pass