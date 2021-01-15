from spotify.api import SpotifyApi
from spotify.auth import User
import sys

# driver file for project

def print_response(endpoint, response):
    print(endpoint)
    print(response.status_code)
    print(response.text)
    print()

if __name__ == "__main__":
    config_file = 'config.json'
    if not (user := User(config_file)).auth():
        sys.exit()
    api = SpotifyApi(user)

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