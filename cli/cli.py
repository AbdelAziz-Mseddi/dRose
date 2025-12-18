import argparse 
parser = argparse.ArgumentParser(
    description="Download your favorite YouTube Music playlists in One Click"
)
parser.add_argument("playlist", help="Add a valid YouTube/YouTube Music playlist URL")
parser.add_argument("--output", "-out", default="downloads", help="Where do you want to save the playlist?")
args=parser.parse_args()