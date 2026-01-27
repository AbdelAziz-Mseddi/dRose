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
        # "python-multipart": ["0.0.9", "0.0.10", False, "multipart"],
        # "PyExecJS": ["1.5.1", "1.6.0",  False, "execjs"] 
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
    #testing typer
    console.print("[CHECKING PYTHON LIBRAIRIES WORK]")
    try:
        import typer
        app=typer.Typer(name="ozymandias")
        @app.command()
        def bcs(name: str, sad: bool = False):
            quote=f"There are so many stars visible in New Mexico,{name}. I will walk out there to get a better look." if sad else f"I travel in worlds you can't even imagine, {name}! You can't conceive of what I'm capable of! I'm so far beyond you! I'm like a god in human clothing! Lightning bolts shoot from my fingertips!"
            typer.echo(quote)
        from typer.testing import CliRunner
        runner=CliRunner()
        result=runner.invoke(app,["kim", "--sad"])
        if("There are so many stars visible in New Mexico,kim. I will walk out there to get a better look." in result.stdout):
            console.print(f"[#347c17]☑  Typer runs correctly.[/#347c17]")
        else:
           console.print(f"[#ffd700]⚠  Typer runs but there may be problems.[/#ffd700]")
    except Exception as e:
            console.print(f"[#b22222]✖  Typer isn't running correctly.[/#b22222]")
    #testing rich
    console.print(f"[#347c17]☑  You are seeing colored output, so Rich probably works correctly.[/#347c17]")
    #testing yt-dlp
    try:
        import yt_dlp
        ydl_opts = {
            'format':"bestaudio/best",  # Format Selection: Best audio only
            'quiet': True,  # Suppress standard output
            'no_warnings': True,  # Suppress warnings
            'ignoreerrors': True,   # Skip private/deleted videos without stopping
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            song=ydl.extract_info("https://music.youtube.com/watch?v=Xr1qIqtnziI&si=cymnEC-gD6xEUZw0", download=False)
            console.print(f"[#347c17]☑  Yt-Dlp runs correctly.[/#347c17]")
    except Exception as e:
        console.print(f"[#b22222]✖  Yt-Dlp isn't running correctly.[/#b22222]")
    #testing ffmpeg
    console.print("[CHECKING FFMPEG WORKS]")
    import shutil
    from pathlib import Path
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        common_paths = [
            "/usr/bin/ffmpeg",
            "/usr/local/bin/ffmpeg",
            "C:\\ffmpeg\\bin\\ffmpeg.exe",
            "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
        ]
        for path in common_paths:
            if Path(path).exists():
                ffmpeg_path = path
                break
    if not ffmpeg_path:
        try:
            import imageio_ffmpeg
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception as e:
            ffmpeg_path = None
    if not ffmpeg_path:
        console.print(f"[#b22222]✖  Ffmpeg isn't found or running correctly.[/#b22222]")
    else:
        try:
            import subprocess
            result = subprocess.run([ffmpeg_path, "-version"], capture_output=True, timeout=5)
            if result.returncode == 0:
                console.print(f"[#347c17]☑  Ffmpeg runs correctly.[/#347c17]")
            else:
                console.print(f"[#b22222]✖  Ffmpeg isn't running correctly.[/#b22222]")
        except Exception as e:
            console.print(f"[#b22222]✖  Ffmpeg isn't running correctly.[/#b22222]")
    #testing permissions
    console.print("[CHECKING FILESYSTEM & PERMISSIONS]")
    import os
    try:
        os.makedirs("temp", exist_ok=True)
        console.print(f"[#347c17]☑  I can make directories :).[/#347c17]")
    except:
        console.print(f"[#b22222]✖   I don't have permission to make directories :(.[/#b22222]")
    try:
        test_file = os.path.join("temp", ".write_test.tmp")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        console.print(f"[#347c17]☑  I can make files :).[/#347c17]")
    except:
        console.print(f"[#b22222]✖   I don't have permission to make files :(.[/#b22222]")
    #testing network and tls
    console.print("[CHECKING NETWORK CONNECTION]")
    import socket, ssl
    host="www.google.com"
    port=443
    timeout=5
    try:
        context=ssl.create_default_context()
        with socket.create_connection( (host, port), timeout=timeout ) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                console.print(f"[#347c17]☑  Da device iz connected zuccessfully.[/#347c17]")
    except:
        console.print(f"[#b22222]✖   I couldn't connect to the network :(.[/#b22222]")
    if (con==False):
        raise typer.Exit(code=1)

#parse version to compare    
def parse_version(version):
    return tuple(map(int, version.split(".")))