# TODO write docstrings

class Album:
    def __init__(self, *, album_type, artists, available_markets, copyrights, external_ids, external_urls, genres, href, images, label, name, popularity, release_date, release_date_precision, restrictions=None, tracks, uri, **kwargs):
        self.album_type = album_type
        self.artists = [SimplifiedArtist(**a) for a in artists]
        self.available_markets = available_markets
        self.copyrights = copyrights
        self.external_ids = ExternalID(**external_ids)
        self.external_urls = ExternalUrl(**external_urls)
        self.genres = genres
        self.href = href
        self.id = kwargs['id']
        self.images = images
        self.label = label
        self.name = name
        self.popularity = popularity
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.restrictions = restrictions
        self.tracks = Paging(**tracks, object_type='simple_track') # spotify api docs lied this isn't an array of tracks
        self.type = kwargs['type']
        self.uri = uri

    def __str__(self):
        return f'{self.album_type} {self.name} by {self.artists}.'

# AlbumRestrictionObject

class Artist:
    def __init__(self, *, external_urls, followers, genres, href, images, name, popularity, uri, **kwargs):
        self.external_urls = ExternalUrl(**external_urls)
        self.followers = Followers(**followers) if followers else None
        self.genres = genres
        self.href = href
        self.id = kwargs['id']
        self.images = images
        self.name = name
        self.popularity = popularity
        self.type = kwargs['type']
        self.uri = uri

    def __str__(self):
        return self.name

# AudioFeaturesObject
# CategoryObject
# ContextObject
# CurrentlyPlayingObject
# CursorObject
# CursorPagingObject
# DeviceObject
# DevicesObject
# EpisodeObject

class ExplicitContentSettings:
    def __init__(self, *, filter_enabled, filter_locked):
        self.filter_enabled = bool(filter_enabled)
        self.filter_locked = bool(filter_locked)

    def __str__(self):
        return 'blocked' if self.filter_enabled else 'not blocked' 

class ExternalID:
    def __init__(self, ean=None, isrc=None, upc=None):
        self.ean = ean # International Article Number
        self.isrc = isrc # International Standard Recording Code
        self.upc = upc # Universal Product Code

class ExternalUrl:
    def __init__(self, **kwargs):
        self.urls = kwargs

    def __str__(self):
        s = ''
        for key, value in self.urls.items():
            s += f'{key}:\t\t{value}\n'
        return s

class Followers:
    def __init__(self, *, href, total):
        self.href = href # always null until spotify implements this
        self.total = int(total)

    def __str__(self):
        return f'No. followers: {self.total}'

class Paging:
    def __init__(self, *, href, items, limit, offset, previous, total, object_type, **kwargs):
        if object_type == 'saved_track': saved_object = SavedTrack
        if object_type == 'saved_album': saved_object = SavedAlbum
        if object_type == 'simple_track' : saved_object = SimplifiedTrack
        if object_type == 'playlist_track' : saved_object = PlaylistTrack
        if object_type == 'playlist' : saved_object = SimplifiedPlaylist

        self.href = href
        self.items = [saved_object(**item) for item in items]
        self.limit = limit
        self.next = kwargs['next']
        self.offset = offset
        self.previous = previous
        self.total = total

# PlayHistoryObject
# PlaylistObject

class PlaylistTrack:
    def __init__(self, *, added_at, added_by, is_local, primary_color, video_thumbnail, track):
        self.added_at = added_at
        self.added_by = added_by
        self.is_local = is_local
        self.primary_color = primary_color # not on the api docs but is needed
        self.video_thumbnail = video_thumbnail #
        self.track = Track(**track)

class PlaylistTracksRef:
    def __init__(self, href, total):
        self.href = href
        self.total = int(total)

class User:
    def __init__(self, *, display_name, external_urls, followers, href, images, uri, country=None, email=None, explicit_content={'filter_enabled':None,'filter_locked':None}, product=None, **kwargs):
        # public attributes
        self.display_name = display_name
        self.external_urls = ExternalUrl(**external_urls)
        self.followers = Followers(**followers)
        self.href = href
        self.id = kwargs['id'] # if only we can unpack to id_ or something..
        self.images = images # unimplemented
        self.type = kwargs['type']
        self.uri = uri
        # private attributes (requires scopes)
        self.country = country  # only if user-read-private
        self.email = email  # user-read-email
        self.explicit_content = ExplicitContentSettings(**explicit_content) # user-read-private
        self.product = product  # user-read-private

    def __str__(self):
        s = ''
        for attr, value in vars(self).items():
            s += f"{attr}:\t\t{value}\n"

        return s

# RecommendationSeedObject
# RecommendationsResponseObject
# ResumePointObject

class SavedAlbum:
    def __init__(self, *, added_at, album):
        self.added_at = added_at
        self.album = Album(**album)

# SavedShowObject

class SavedTrack:
    def __init__(self, *, added_at, track):
        self.added_at = added_at
        self.track = Track(**track)

    def __str__(self):
        return f'Saved {self.track} at {self.added_at}'

# ShowObject

class SimplifiedAlbum:
    def __init__(self, *, album_group=None, album_type, artists, available_markets=None, external_urls, href, images, name, restrictions=None, uri, **kwargs):
        self.album_group = album_group
        self.album_type = album_type
        self.artists = artists # TODO array of simplified artist object
        self.available_markets = available_markets
        self.external_urls = ExternalUrl(**external_urls)
        self.href = href
        self.id = kwargs['id']
        self.images = images # unimplemented
        self.name = name
        self.restrictions = restrictions # TODO restriction object / only when restriction is applied
        self.type = kwargs['type']
        self.uri = uri

    def __str__(self):
        return self.name if self.album_type != 'single' else ''

class SimplifiedArtist:
    def __init__(self, *, external_urls, href, name, uri, **kwargs):
        self.external_urls = ExternalUrl(**external_urls)
        self.href = href
        self.id = kwargs['id']
        self.name = name
        self.type = kwargs['type']
        self.uri = uri

    def __str__(self):
        return self.name

class SimplifiedPlaylist:
    def __init__(self, *, collaborative, description, external_urls, href, images, name, owner, public, snapshot_id, tracks, uri, **kwargs):
        self.collaborative = bool(collaborative)
        self.description = description
        self.external_urls = ExternalUrl(**external_urls)
        self.href = href
        self.id = kwargs['id']
        self.images = images
        self.name = name
        self.owner = owner
        self.public = public
        self.snapshot_id = snapshot_id
        self.tracks = PlaylistTracksRef(**tracks)
        self.type = kwargs['type']
        self.uri = uri

# SimplifiedEpisodeObject
# SimplifiedShowObject

class SimplifiedTrack:
    def __init__(self, *, artists, available_markets, disc_number, duration_ms, explicit, external_urls, href, is_local, is_playable=None, linked_from=None, name, preview_url, restrictions=None, track_number, uri, **kwargs):
        self.artists = [SimplifiedArtist(**a) for a in artists]
        self.available_markets = available_markets
        self.disc_number = disc_number
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.external_urls = ExternalUrl(**external_urls)
        self.href = href
        self.id = kwargs['id']
        self.is_local = is_local
        self.is_playable = is_playable
        self.linked_from = linked_from
        self.name = name
        self.preview_url = preview_url
        self.restrictions = TrackRestriction(restrictions)
        self.track_number = track_number
        self.type = kwargs['type']
        self.uri = uri

class Track:
    def __init__(self, *, album, artists, available_markets=None, disc_number, duration_ms, explicit, external_ids, external_urls, href, is_local, is_playable=None, linked_from=None, name, popularity, preview_url, restrictions=None, track_number, uri, json=None, **kwargs):
        self.album = SimplifiedAlbum(**album)
        self.artists = [SimplifiedArtist(**a) for a in artists]
        self.available_markets = available_markets
        self.disc_number = disc_number
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.external_ids = ExternalID(**external_ids)
        self.external_urls = ExternalUrl(**external_urls)
        self.href = href
        self.id = kwargs['id']
        self.is_local = is_local
        self.is_playable = is_playable # only if track linking is applied
        self.linked_from = linked_from # ^
        self.name = name
        self.popularity = popularity
        self.preview_url = preview_url
        self.restrictions = TrackRestriction(restrictions)
        self.track_number = track_number
        self.type = kwargs['type']
        self.uri = uri
        self.json = json

    def __str__(self):
        return f'{self.name} by {"&".join([str(a) for a in self.artists])}.'

class TrackRestriction:
    def __init__(self, reason):
        self.reason = reason # one of: market, product or explicit

# TuneableTrackObject