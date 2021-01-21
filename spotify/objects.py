# TODO write docstrings

# AlbumObject
# AlbumRestrictionObject

class Artist:
    # apparently these four attributes are part of the object according to spotify, but not given
    def __init__(self, *, external_urls, followers=None, genres=None, href, images=None, name, popularity=None, uri, **kwargs):
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
        # these attributes are unused by spotify ??
        if self.followers or self.genres or self.images or self.popularity:
            return f'{self.name.encode("utf-8")} DEBUG {self.followers} {self.genres} {self.images} {self.popularity}'
        return f'{self.name.encode("utf-8")}'

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

# ExternalIdObject

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

# assumes all paged items are saved track objects
class Paging:
    def __init__(self, *, href, items, limit, offset, previous, total, **kwargs):
        self.href = href
        self.items = [SavedTrack(**item) for item in items]
        self.limit = limit
        self.next = kwargs['next']
        self.offset = offset
        self.previous = previous
        self.total = total

# PlayHistoryObject
# PlaylistObject
# PlaylistTrackObject

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
# SavedAlbumObject
# SavedShowObject

class SavedTrack:
    def __init__(self, *, added_at, track):
        self.added_at = added_at
        self.track = Track(**track)

    def __str__(self):
        return f'Saved {self.track} at {self.added_at}'

# ShowObject

class SimplifiedAlbum:
    def __init__(self, *, album_group=None, album_type, artists, available_markets, external_urls, href, images, name, restrictions=None, uri, **kwargs):
        self.album_group = album_group
        self.album_type = album_type
        self.artists = artists # TODO array of simplified artist object
        self.available_markets = available_markets
        self.external_urls = ExternalUrl(**external_urls)
        self.href = href
        self.id = kwargs['id']
        self.images = images # unimplemented
        self.restrictions = restrictions # TODO restriction object / only when restriction is applied
        self.type = kwargs['type']
        self.uri = uri

# SimplifiedEpisodeObject
# SimplifiedShowObject
# SimplifiedTrackObject

class Track:
    def __init__(self, *, album, artists, available_markets, disc_number, duration_ms, explicit, external_ids, external_urls, href, is_playable=None, linked_from=None, name, popularity, preview_url, restrictions=None, track_number, uri, **kwargs):
        self.album = SimplifiedAlbum(**album)
        self.artists = [Artist(**a) for a in artists]
        self.available_markets = available_markets
        self.disc_number = disc_number
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.external_ids = external_ids # TODO external id object
        self.external_urls = ExternalUrl(**external_urls)
        self.href = href
        self.id = kwargs['id']
        self.is_playable = is_playable # only if track linking is applied
        self.linked_from = linked_from # ^
        self.name = name
        self.popularity = popularity
        self.preview_url = preview_url
        self.restrictions = restrictions # TODO restriction object / only if restrictions is enabled
        self.track_number = track_number
        self.type = kwargs['type']
        self.uri = uri

    def __str__(self):
        return f'{self.name.encode("utf-8")} by {self.artists} available at {self.external_urls}'

# TrackRestrictionObject
# TuneableTrackObject