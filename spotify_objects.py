### contains all the 

# AlbumObject
# AlbumRestrictionObject
# ArtistObject
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

class ExternalURL:
    def __init__(self, **kwargs):
        self.type = list(kwargs)[0]
        self.url = kwargs[self.type]

        # all examples I have seen only have the single url
        # if not...
        self.urls = kwargs

    def __str__(self):
        return self.url

class Followers:
    def __init__(self, *, href, total):
        self.href = href # always null until spotify implements this
        self.total = int(total)

    def __str__(self):
        return f'No.: {self.total}'

# PagingObject
# PlayHistoryObject
# PlaylistObject
# PlaylistTrackObject

class User:
    def __init__(self, *, display_name, external_urls, followers, href, images, uri, country=None, email=None, explicit_content={'filter_enabled':None,'filter_locked':None}, product=None, **kwargs):
        # public attributes
        self.display_name = display_name
        self.external_urls = ExternalURL(**external_urls)
        self.followers = Followers(**followers)
        self.href = href
        self.id = kwargs['id'] # if only we can unpack to id_ or something..
        self.images = images # unimplemented
        self.type = kwargs['type']
        self.uri = uri
        # private attributes (requires scopes)
        self.country = country  # user-read-private
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
# SavedTrackObject
# ShowObject
# SimplifiedAlbumObject
# SimplifiedEpisodeObject
# SimplifiedShowObject
# SimplifiedTrackObject
# TrackObject
# TrackRestrictionObject
# TuneableTrackObject