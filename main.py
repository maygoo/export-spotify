from spotify.api import SpotifyApi
from spotify.auth import User
from spotify.objects import Track
from urllib.parse import urlparse, parse_qs
import sys, os, csv, argparse

# driver file for project

def track_to_csv(track: Track):
    print(track.name)

def get_library_all(api: SpotifyApi):
    library = []

    paging = api.get_library()
    print(f"Collecting all {paging.total} liked songs...")

    while paging.next:
        paged_items = [st.track for st in paging.items]
        library += paged_items
        offset = parse_qs(urlparse(paging.next).query)['offset']
        paging = api.get_library(offset)
    paged_items = [st.track for st in paging.items]
    library += paged_items

    print(f"Done. Collected {len(library)} songs.")
    for i in library: track_to_csv(i)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # TODO add options for exporting only library, playlists, etc
    parser.add_argument('outfile', help='file to export the song list to')
    args = parser.parse_args()

    if os.path.isfile(args.outfile):
        print(f"WARNING: The file '{args.outfile}' already exists and will be overwritten.\nPress enter to continue.")
        input()

    config_file = 'config.json'
    if not (user := User(config_file)).auth():
        sys.exit()
    api = SpotifyApi(user)

    #print(api.get_me())
    #get_library_all(api)
    track = api.get_track('6EOKwO6WaLal58MSsi6U4W')
    track_to_csv(track)
