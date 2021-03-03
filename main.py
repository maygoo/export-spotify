from spotify.api import SpotifyApi
from spotify.auth import User
from spotify.objects import Track
from urllib.parse import urlparse, parse_qs
import sys, os, csv, argparse

# driver file for project

def track_to_csv(track: Track):
    return (track.name, str(track.album), ' & '.join([str(a) for a in track.artists]), track.href, track.external_ids.ean, track.external_ids.isrc, track.external_ids.upc)

def songlist_to_csv(songlist):
    return set([track_to_csv(t) for t in songlist]) # removes duplicates

def write_to_file(filename, csvlist):
    header = ['name','album','artists','href','ean','isrc','upc']

    print(f"Writing {len(csvlist)} songs to {filename}.")

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(csvlist)
    print("Done.")

def get_all_albums(api: SpotifyApi):
    paging = api.get_saved_albums()
    print(f"Collecting all {paging.total} saved albums...")

    albums = [sa.album for sa in de_paging(api.get_saved_albums, paging)]

    print(f"Done. Collected {len(albums)} albums.")
    return albums

def get_songlist_from_albums(api):
    albums = get_all_albums(api)
    songlist = []
    for i in albums:
        temp_list = []
        print(f"Collecting all {i.tracks.total} songs in the {i.album_type} {i.name}...")
        temp_list = de_paging(api.get_album_tracks, i.tracks, i.id)
        print(f"Done. Collected {len(temp_list)} songs.")
        songlist += temp_list

    return songlist

def fix_album_songlist(api, songlist):
    # make each simple track into track
    # to add album and external id attributes
    new_songlist = []
    for i in songlist:
        new_songlist.append(api.get_track(i.id)) # TODO get tracks in bulk to speed this up
    return new_songlist

def get_library_all(api):
    paging = api.get_library()
    print(f"Collecting all {paging.total} liked songs...")

    library = [st.track for st in de_paging(api.get_library, paging)]

    print(f"Done. Collected {len(library)} songs.")
    return library

def de_paging(source, paging, album=False):
    out = []

    while paging.next:
        paged_items = paging.items
        out += paged_items
        offset = parse_qs(urlparse(paging.next).query)['offset']
        offset = (album, offset) if album else offset # album paging awkwardness
        paging = source(offset)
    paged_items = paging.items
    out += paged_items
    return out

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

    library = get_library_all(api)
    album_songlist = fix_album_songlist(api, get_songlist_from_albums(api))
    
    full_songlist = library + album_songlist
    print(len(full_songlist))
    write_to_file(args.outfile, songlist_to_csv(full_songlist))