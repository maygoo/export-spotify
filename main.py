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
    print_response(*api.me())
    print_response(*api.user('tzpug32uzycy3ldd9xacoj0xz')) # follow me on spotify ;)