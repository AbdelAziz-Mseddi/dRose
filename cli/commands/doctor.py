import typer
app=typer.Typer(
    name="doctor",
    help="i am here to check your device's compatibility for Top-Tier Music :p",
    no_args_is_help=True,
    add_completion=False
)

supportedOS={
    "windows":{"min": 7},
    "linux": 1,
    "Darwin": {"min": 10.9} #macOS
}

@app.command(invoke_without_command=True)
def check():
    """check system requirements"""
    pass