from spotify_api import SpotifyApi
import sys

# driver file for project

if __name__ == "__main__":
    config_file = 'config.json'
    api = SpotifyApi(config_file)
    if not api.auth():
        sys.exit()