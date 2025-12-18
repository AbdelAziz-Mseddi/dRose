import argparse 
parser = argparse.ArgumentParser(
    description="Dwonload your favorite YouTube Music playlists in One Click"
)
parser.add_argument("playlist", help="Add a valid YouTube/YouTube Music playlist URL")
args=parser.parse_args()