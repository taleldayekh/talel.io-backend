from enum import Enum


class ActivityPubObject(Enum):
    '''
    Object types in ActivityPub represent
    different form of content that can be
    created, shared, liked, or interacted
    with. Full list of object types:

    https://www.w3.org/TR/activitystreams-vocabulary/#object-types
    '''
    NOTE = 'Note'
