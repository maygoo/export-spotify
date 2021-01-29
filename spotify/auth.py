# auth only makes sense within a client, so client info is also stored here

import json
import webbrowser
import json
import datetime
import requests

class User:
    _auth_url = 'https://accounts.spotify.com'
    _redirect = 'https://localhost/' # incorporate into github.io page

    def __init__(self, config_file=None):
        """Create auth object from given file. If no file is given, prompt user for info."""
        self._config_file = config_file
        self._client_id = None
        self._client_secret = None
        self._user_auth = None
        self._user_refresh = None
        self._user_access = None
        # internal timer kept for refresh key
        self._expires = None

    def auth(self):
        """Load auth from config file. Prompt user for log in if required."""

        # check config
        try:
            with open(self._config_file, 'r') as f:
                config = json.load(f)
                self._client_id = config['client_id']
                self._client_secret = config['client_secret']
                self._user_auth = config['user_auth']
                self._user_refresh = config['user_refresh']
        except Exception as e:
            print(e)
            print(f"Error: unable to read config file '{self._config_file}'")
            # TODO manual input

        if self._user_refresh: return self._refresh()
        elif self._user_auth: return self._refresh(True)
        else: return self._prompt_login() and self._refresh(True)

    def _prompt_login(self):
        """Prompt user to log in and get authorisation code. Return true if successful."""
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

        query = {
            'client_id' : self._client_id,
            'response_type' : 'code',
            'redirect_uri' : User._redirect,
            'scope' : '+'.join(scopes)
        }

        query = '&'.join([f'{key}={query[key]}' for key in query.keys()])
        url = User._auth_url+endpoint+'?'+query

        print("\nInitial authorisation required")
        print(f"Opening up a browser\nIf nothing happens for a few moments, please manually visit the url: {url}")
        webbrowser.open(url)
        print("Please sign in to your spotify account and allow the permissions")
        print("You will be redirected to a page that is unable to load")
        self._user_auth = input("Please copy the url of this page, and paste the part after 'https://localhost/?code=' here:\n")
        print("This authorisation code is being saved to your config file")

        if not self._save_config(): return False

        print(f"Saved auth to {self._config_file}")
        return True

    def _refresh(self, initial=False):
        """Request access token. Return true if successful."""
        endpoint = '/api/token'

        # get access token from initial auth code or from refresh code

        body = {
            'client_id' : self._client_id,
            'client_secret' : self._client_secret
        }

        if initial:
            body['grant_type'] = 'authorization_code'
            body['code'] = self._user_auth
            body['redirect_uri'] = User._redirect
        else:
            body['grant_type'] = 'refresh_token'
            body['refresh_token'] = self._user_refresh
        

        response = requests.request('POST', self._auth_url+endpoint, data=body)

        if not response.ok:
            raise AccessError(response)
        
        content = json.loads(response.content)
        if initial: 
            self._user_refresh = content['refresh_token']
        self._user_access = content['access_token']

        # get new refresh key 1 minute before it expires
        duration = datetime.timedelta(seconds=int(content['expires_in']) - 60)
        self._expires = datetime.datetime.now() + duration

        if initial: return self._save_config()
        return True

    # save auth tokens to file
    def _save_config(self):
        """Save config values. Return false if unable to write to file."""
        config = {
            "client_id" : self._client_id,
            "client_secret" : self._client_secret,
            "user_auth" : self._user_auth,
            "user_refresh" : self._user_refresh
        }

        try:
            with open(self._config_file, 'w') as f:
                json.dump(config, f)
        except:
            print(f"Unable to save your config file. Please manually enter the auth code {self._user_auth} and/or refresh token {self._user_refresh} in {self._config_file}")
            return False
        return True

    def get_access(self):
        """Return access token. Generate new one if necessary."""
        if True if self._expires is None else (datetime.datetime.now() > self._expires): self._refresh()
        return self._user_access


class AccessError(Exception):
    """Exception raised when unable to get new access token."""
    
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f"Unable to obtain access token. {self.response.status_code} full response:\n{self.response.text}"