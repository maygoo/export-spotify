from spotify.api import SpotifyApi
from spotify.auth import User
from urllib.parse import urlparse, parse_qs
import sys

# driver file for project

# don't remember why I had this function
def print_response(endpoint, response):
    print(endpoint)
    print(response.status_code)
    print(response.text)
    print()

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
    for i in library: print(i)

if __name__ == "__main__":
    config_file = 'config.json'
    if not (user := User(config_file)).auth():
        sys.exit()
    api = SpotifyApi(user)

    # calling all api functions
    print(api.get_me())
    
    get_full_library(api)