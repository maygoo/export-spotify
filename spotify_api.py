import requests
import webbrowser
import json
import datetime

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
        # internal timer kept for refresh key
        self.expires = None

    # requests a user authorisation code, prompts user to login
    def auth(self, force=False):
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
        if not force and (self.user_refresh or self.user_auth):
            print(f"Successfully loaded user auth from {self.config_file}")
            return True

        endpoint = '/authorize'

        scopes = [
            'user-read-email',              # used to categorise song by spotify account
            'user-read-private',            # used to get user explicit content settings
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
        self.user_auth = input("Please copy the url of this page, and paste the part after 'https://localhost/?code=code=' here:\n")
        print("This authorisation code is being saved to your config file")

        # assume auth succeeds

        if not self.save_config(): return False

        print(f"Successfully saved auth to {self.config_file}")

        return self.refresh()

    # requests new access and refresh tokens
    def refresh(self):
        endpoint = '/api/token'

        refresh = bool(self.user_refresh)

        # can get access token from initial auth code or from refresh code

        body = {
            'client_id' : self.client_id,
            'client_secret' : self.client_secret
        }

        if refresh:
            body['grant_type'] = 'refresh_token'
            body['refresh_token'] = self.user_refresh
        else:
            body['grant_type'] = 'authorization_code'
            body['code'] = self.user_auth
            body['redirect_uri'] = SpotifyApi.redirect

        response = requests.request('POST', self.auth_url+endpoint, data=body)

        if not response.ok:
            print(response.status_code, response.text)
            print("Unable to obtain refresh key")
            return False
        
        content = json.loads(response.content)
        if not refresh: self.user_refresh = content['refresh_token']
        self.user_access = content['access_token']

        # get new refresh key 1 minute before it expires
        duration = datetime.timedelta(seconds=int(content['expires_in']) - 60)
        self.expires = datetime.datetime.now() + duration

        if not refresh and not self.save_config(): return False
        return True

    def save_config(self):
        config = {
            "client_id" : self.client_id,
            "client_secret" : self.client_secret,
            "user_auth" : self.user_auth,
            "user_refresh" : self.user_refresh
        }

        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except:
            print(f"Unable to save your config file. Please manually enter the auth code {self.user_auth} in {self.config_file}")
            return False
        return True

    # request wrapper function to add access key refresh when needed
    def auth_request(self, method, endpoint, **kwargs):
        if True if self.expires is None else (datetime.datetime.now() > self.expires): self.refresh()

        headers = {
            'Authorization' : f'Bearer {self.user_access}'
        }

        return requests.request(method, self.api_url+endpoint, headers=headers, **kwargs)

###
###  implementation of spotify functions
###

## user profile
# todo create and return user objects 

    # Get detailed profile information about the current user (including the current user’s username).
    # scopes used:  user-read-email     (opt)
    #               user-read-private   (opt)
    def me(self):
        endpoint = '/v1/me'

        response = self.auth_request('GET', endpoint)

        return endpoint, response

    # Get public profile information about a Spotify user.
    def user(self, user_id):
        endpoint = f'/v1/users/{user_id}'

        response = self.auth_request('GET', endpoint)

        return endpoint, response
