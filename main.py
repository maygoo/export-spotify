from spotify_api import SpotifyApi
import sys

# driver file for project

def print_response(endpoint, response):
    print(endpoint)
    print(response.status_code)
    print(response.text)
    print()

if __name__ == "__main__":
    config_file = 'config.json'
    api = SpotifyApi(config_file)
    if not api.auth():
        sys.exit()

    # calling all api functions
    print(api.get_me())
    print(api.get_user('foo'))
    paging = api.get_library(0,10)
    items = paging.items
    saved_track = items[0]
    track = saved_track.track
    print(items)
    print()
    print(saved_track)
    print()
    print(track)