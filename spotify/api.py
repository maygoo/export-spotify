from spotify.auth import User
import spotify.objects as so
import requests
import json

class SpotifyApi:
    _api_url = 'https://api.spotify.com'

    def __init__(self, auth):
        self._auth: User = auth

    # request wrapper function to add access key refresh when needed
    def _auth_request(self, method, endpoint, **kwargs):
        headers = {
            'Authorization' : f'Bearer {self._auth.get_access()}'
        }

        response = requests.request(method, self._api_url+endpoint, headers=headers, **kwargs)

        if not response.ok:
            print(f"Error: Call to {endpoint} returned with status code {response.status_code}. Full response:\n{response.text}")
            return False

        return response

###
###  implementation of spotify functions
###

## albums
# Get Multiple Albums
# Get an Album
# Get an Album's Tracks

## artists
# Get Multiple Artists
# Get an Artist
# Get an Artist's Top Tracks
# Get an Artist's Related Artists
# Get an Artist's Albums

## browse
# Get All New Releases
# Get All Featured Playlists
# Get All Categories
# Get a Category
# Get a Category's Playlists
# Get Recommendations
# Get Recommendation Genres

## episodes
# Get Multiple Episodes
# Get an Episode

## follow
# Follow a Playlist
# Unfollow Playlist
# Check if Users Follow a Playlist
# Get User's Followed Artists
# Follow Artists or Users
# Unfollow Artists or Users
# Get Following State for Artists/Users

## library
# Get User's Saved Albums
# Save Albums for Current User
# Remove Albums for Current User
# Check User's Saved Albums

    # Get a list of the songs saved in the current Spotify user’s ‘Your Music’ library.
    # scopes used:  user-library-read
    def get_library(self, offset=0, limit=50):
        endpoint = '/v1/me/tracks'

        query = {
            'offset' : offset,
            'limit' : limit
        }

        response = self._auth_request('GET', endpoint, params=query)

        return so.Paging(**json.loads(response.content)) if response else False
        

# returns an array of saved track objects
# wrapped in a paging object

# Save Tracks for User
# Remove User's Saved Tracks
# Check User's Saved Tracks
# Get User's Saved Shows
# Save Shows for Current User
# Remove User's Saved Shows
# Check User's Saved Shows

## personalisation
# Get a User's Top Artists and Tracks

## player
# Get Information About The User's Current Playback
# Transfer a User's Playback
# Get a User's Available Devices
# Get the User's Currently Playing Track
# Start/Resume a User's Playback
# Pause a User's Playback
# Skip User’s Playback To Next Track
# Skip User’s Playback To Previous Track
# Seek To Position In Currently Playing Track
# Set Repeat Mode On User’s Playback
# Set Volume For User's Playback
# Toggle Shuffle For User’s Playback
# Get Current User's Recently Played Tracks
# Add an item to queue

## playlists
# Get a List of Current User's Playlists
# Get a List of a User's Playlists
# Create a Playlist
# Get a Playlist
# Change a Playlist's Details
# Get a Playlist's Items
# Add Items to a Playlist
# Reorder or Replace a Playlist's Items
# Remove Items from a Playlist
# Get a Playlist Cover Image
# Upload a Custom Playlist Cover Image

## search
# Search for an Item

## shows
# Get Multiple Shows
# Get a Show
# Get a Show's Episodes

## tracks
# Get Several Tracks
# Get a Track
# Get Audio Features for Several Tracks
# Get Audio Features for a Track
# Get Audio Analysis for a Track

## user profile

    # Get detailed profile information about the current user (including the current user’s username).
    # scopes used:  user-read-email     (opt)
    #               user-read-private   (opt)
    def get_me(self):
        endpoint = '/v1/me'

        response = self._auth_request('GET', endpoint)

        return so.User(**json.loads(response.content)) if response else False

    # Get public profile information about a Spotify user.
    def get_user(self, user_id):
        endpoint = f'/v1/users/{user_id}'

        response = self._auth_request('GET', endpoint)

        return so.User(**json.loads(response.content)) if response else False