import requests
import webbrowser
import json

# handles api requests

class SpotifyApi:
    api_url = 'https://api.spotify.com'
    auth_url = 'https://accounts.spotify.com'
    redirect = 'https://localhost/' # fix later

    def __init__(self, config_file):
        self.config_file = config_file
        self.client_id = None
        self.client_secret = None
        self.user_auth = None
        self.user_refresh = None
        self.user_access = None

    # requests a user authorisation code, prompts user to login
    def auth(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.client_id = config['client_id']
                self.client_secret = config['client_secret']
                self.user_auth = config['user_auth']
                self.user_refresh = config['user_refresh']
        except:
            print(f"Unable to read config file '{self.config_file}'")
            return False

        # no need to authenticate if tokens exist
        if self.user_refresh or self.user_auth:
            print(f"Successfully loaded user auth from {self.config_file}")
            return True

        endpoint = '/authorize'

        scopes = [
            'user-read-email',              # used to categorise song by spotify account
            'playlist-read-private',        # used to get list of songs in playlists
            'user-library-read',            # used to get list of 'your music'/liked songs
            'playlist-read-collaborative']  # used to get list of songs in shared playlists
        # note on scopes: currently these are all read-only, 
        # might change in the future if I decide to implement
        # playlist/liked songs import

        response_type = 'code' # required

        query = {
            'client_id' : self.client_id,
            'response_type' : response_type,
            'redirect_uri' : SpotifyApi.redirect,
            'scope' : '+'.join(scopes)
        }

        query = '&'.join([f'{key}={query[key]}' for key in query.keys()])

        print("Initial authentication required")
        print(f"Opening up a browser (if nothing happens for a few moments, please manually visit the url: {SpotifyApi.auth_url+endpoint+query}")
        webbrowser.open(SpotifyApi.auth_url+endpoint+'?'+query)
        print("Please sign in to your spotify account and allow the permissions")
        print("You will be redirected to a page that is unable to load")
        self.user_auth = input("Please copy the url of this page, and paste the part after 'code=' here:\n")
        print("This authorisation code is being saved to your config file")

        config = {
            "client_id" : self.client_id,
            "client_secret" : self.client_secret,
            "user_auth" : self.user_auth,
            "user_refresh" : self.user_refresh
        }

        # assume auth succeeds

        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except:
            print(f"Unable to save your config file. Please manually enter the auth code {self.user_auth} in {self.config_file}")
            return False

        print(f"Successfully saved auth to {self.config_file}")

        self.refresh()
        return True

    # requests new access and refresh tokens
    def refresh(self):
        endpoint = '/api/token'

        body = {
            'grant_type' : 'authorization_code',
            'code' : self.user_auth,                # authorisation code or refresh key if one exists
            'redirect_uri' : SpotifyApi.redirect,   
            'client_id' : self.client_id,
            'client_secret' : self.client_secret
        }

        headers = {}

        #response = requests.request('POST', self.auth_url, data=body, headers=headers)

        #print(response.status_code)
        #print(response.text)



        # POST

# each api call should check if the access key has expired and get a new one if it has