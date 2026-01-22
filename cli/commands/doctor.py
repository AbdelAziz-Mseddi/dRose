import typer
import platform
from rich.console import Console
import sys

app=typer.Typer(
    name="doctor",
    help="i am here to check your device's compatibility for Top-Tier Music :p",
    no_args_is_help=True,
    add_completion=False
)
console=Console()
supportedOS={
    "windows":{"tested": True, "min": 7},
    "linux": {"tested": False, "min": 112263},#i am the best mini-series, who am i? :p
    "Darwin": {"tested": True, "min": 10.9} #macOS
}

@app.command(invoke_without_command=True)
def check():
    """check system requirements"""
    #check system architecture and operating system
    os_name=platform.system()
    os_release=platform.release()
    archi=platform.architecture()[0]
    con=True
    if (archi is not "64bit"):
        console.print("[#b22222]✖ Architecture not supported. Please use 64-bit.[/#b22222]")
        con=False
    if( supportedOS[os_name].get("tested") and os_release < supportedOS[os_name].get("min") ):
        console.print(f"[#b22222]✖ {os_name} release not supported. Please upgrade to {supportedOS[os_name].get("min")} minimum.[/#b22222]")
        con=False
    elif ( not supportedOS[os_name].get("tested") ):
        console.print(f"[#ffd700 ]⚠ Proceed with caution, untested OS[/#ffd700 ]")
    #check Python interpreter
    min_major=3
    min_minor=9
    version_tuple=sys.version_info
    major=version_tuple.major
    minor=version_tuple.minor
    if( major < min_major ):
        console.print("[#b22222]✖ Python version not supported. Minimum version is <3.9>.[/#b22222]")
        con=False
    elif( minor < min_minor ):
        console.print("[#b22222]✖ Python version not supported. Minimum version is <3.9>.[/#b22222]")
        con=False
    #check python packages (requirements)
    packages = [
    "typer",
    "rich",
    "yt-dlp",
    "imageio-ffmpeg",
    "tqdm",
    "python-multipart",
    "PyExecJS"
    ]
    for package in packages:
        try:
            __import__(package)
        except ImportError as e:
            console.print(f"[#b22222]✖ Required package missing. Please install {package}.[/#b22222]")
            con=False
    if (con==False):
        raise typer.Exit(code=1)
    