import typer
import platform
from rich.console import Console
import sys
import importlib.metadata

app=typer.Typer(
    name="doctor",
    help="i am here to check your device's compatibility for Top-Tier Music :p"
)
console=Console()
supportedOS={
    "Windows":{"tested": True, "min": 7},
    "Linux": {"tested": False, "min": 112263},#i am the best mini-series, who am i? :p
    "Darwin": {"tested": True, "min": 10.9} #macOS
}

@app.callback(invoke_without_command=True)
def check():
    """check system requirements"""
    console.print("[#6594B1]🥀 You summoned the doctor command? Have no fear, it won't hurt.[/#6594B1]")
    #check system architecture and operating system
    console.print("[CHECKING TOUSKIE SYSTEM]")
    os_name=platform.system()
    os_release=platform.release()
    archi=platform.architecture()[0]
    con=True
    if (archi != "64bit"):
        console.print("[#b22222]✖  Architecture not supported. Please use 64-bit.[/#b22222]")
        con=False
    else :
        console.print("[#347c17]☑  System Architecture is supported.[/#347c17]")
    if( supportedOS[os_name].get("tested") and int(os_release) < supportedOS[os_name].get("min") ):
        console.print(f"[#b22222]✖  {os_name} release not supported. Please upgrade to {supportedOS[os_name].get("min")} minimum.[/#b22222]")
        con=False
    elif ( not supportedOS[os_name].get("tested") ):
        console.print("[#ffd700]⚠  Proceed with caution, untested OS.[/#ffd700]")
    else :
        console.print("[#347c17]☑  Operating System is supported.[/#347c17]")
    #check Python interpreter
    console.print("[CHECKING PYTHON INTERPRETER]")
    min_major=3
    min_minor=9
    version_tuple=sys.version_info
    major=version_tuple.major
    minor=version_tuple.minor
    if( major < min_major ):
        console.print("[#b22222]✖  Python version not supported. Minimum version is <3.9>.[/#b22222]")
        con=False
    elif( minor < min_minor ):
        console.print("[#b22222]✖  Python version not supported. Minimum version is <3.9>.[/#b22222]")
        con=False
    else:
        console.print(f"[#347c17]☑  Your Python version is supported.[/#347c17]")
    #check python packages (requirements) are imported
    console.print("[CHECKING TOUSKIE PYTHON LIBRAIRIES]")
    packages = {
        "typer": ["0.9.0", "1.0.0", False, "typer"],   #(min, max, import successful, import alias)
        "rich": ["13.7.0", "14.0.0", False, "rich"],
        "yt-dlp": ["2024.11.18", "2026.0.0", False, "yt_dlp"], 
        "imageio-ffmpeg": ["0.4.9", "0.5.0", False, "imageio_ffmpeg"],
        "tqdm": ["4.66.1", "4.66.1", False, "tqdm"], 
        "python-multipart": ["0.0.9", "0.0.10", False, "multipart"],
        "PyExecJS": ["1.5.1", "1.6.0",  False, "execjs"] 
    }
    for package in packages.keys():
        try:
            __import__(packages[package][3])
            packages[package][2]=True
        except ImportError as e:
            console.print(f"[#b22222]✖  Required package missing. Please install {package}.[/#b22222]")
            con=False
    #check python packages versions
    for package in packages:
        if packages[package][2]:
            act_ver=parse_version( importlib.metadata.version(package) )
            min_ver=parse_version( packages[package][0] )
            max_ver=parse_version( packages[package][1] )
            if(min_ver==max_ver):
                if( act_ver!=min_ver ):
                    console.print(f"[#ffd700]⚠  {package} version may cause problems. Recommended vesion= {packages[package][0]}.[/#ffd700]")                
                else:
                    console.print(f"[#347c17]☑  {package} is installed, version is compatible.[/#347c17]")
            elif(act_ver<min_ver or act_ver>max_ver):
                console.print(f"[#ffd700]⚠  {package} version may cause problems. Recommended version >= {packages[package][0]} and < {packages[package][1]}.[/#ffd700]")
            else:
                console.print(f"[#347c17]☑  {package} is installed, version is compatible.[/#347c17]")
    if (con==False):
        raise typer.Exit(code=1)

#parse version to compare    
def parse_version(version):
    return tuple(map(int, version.split(".")))