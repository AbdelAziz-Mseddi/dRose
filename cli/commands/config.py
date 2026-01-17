import typer
from cli import config_store as conf
from rich.console import Console

app = typer.Typer(
    name="config",
    help="i am in charge of your default configuration :p",
    no_args_is_help=True,
    add_completion=False
)

console=Console()

@app.command()
def set(
    output_folder: str = typer.Option(None, "--output-folder", "-o", help="Default output folder for downloads"),
    audio_format: str = typer.Option(None, "--audio-format", "-f", help="Default audio format"),
        ):
    """set user configuration(overrides the default)"""
    updates = {"output_folder": output_folder, "audio_format": audio_format}
    if all(v is None for v in updates.values()):
        console.print("[#FA5C5C]No settings provided. Use --output-folder or --audio-format.[/#FA5C5C]")
        raise typer.Exit(1)

    merged = conf.set_config(updates)
    if output_folder is not None:
        console.print(f"[#A8DF8E]ø Output Folder set to: {merged[0].get('output_folder')}[/#A8DF8E]")
    if audio_format is not None:
        console.print(f"[#A8DF8E]ø Audio Format set to: {merged[0].get('audio_format')}[/#A8DF8E]")


@app.command()
def get(setting: str = typer.Argument(..., help="Setting name (output_folder or audio_format)")):
    """get the value of a specific setting from current user configuration"""
    value = conf.get_setting(setting)
    if value is None:
        console.print(f"[#FA5C5C]Setting '{setting}' not found.[/#FA5C5C]")
        raise typer.Exit(1)
    console.print(f"[#A8DF8E]ø {setting}: {value}[/#A8DF8E]")


@app.command()
def show():
    """show current user configuration"""
    merged,eq = conf.get_config()
    if not merged:
        console.print("[#FA5C5C]No configuration available.[/#FA5C5C]")
        raise typer.Exit(1)
    if(eq):
        console.print("[#A8DF8E]Default configuration is set as the Current Configuration[/#A8DF8E]")
    console.print("[#A8DF8E]Current Configuration:[/#A8DF8E]")
    for k, v in merged.items():
        console.print(f"[#F0FFDF] ø {k}: {v}[/#F0FFDF]")