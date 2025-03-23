from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, TypedDict


class Platform(str, Enum):
    BLUESKY = 'bluesky'
    MASTODON = 'mastodon'
    PIXELFED = 'pixelfed'


class MediaType(str, Enum):
    IMAGE = 'image'
    VIDEO = 'video'


class Media(TypedDict):
    url: str
    type: MediaType
    alt: str


class Audience(TypedDict):
    to: List[str]
    cc: List[str]


class Post(TypedDict):
    content: Optional[str]
    media: List[Media]
    audience: Audience


@dataclass
class MediaModel:
    url: str
    type: MediaType
    alt: str


@dataclass
class AudienceModel:
    to: List[str] = field(default_factory=list)
    cc: List[str] = field(default_factory=list)


@dataclass
class PostModel:
    platforms: List[Platform]
    content: Optional[str] = None
    media: List[MediaModel] = field(default_factory=list)
    audience: AudienceModel = field(default_factory=AudienceModel)

    def __post_init__(self) -> None:
        '''
        Defaults Mastodon and Pixelfed posts to a
        public audience if "to" is not specified.
        '''
        if not self.audience.to:
            self.audience.to = ['https://www.w3.org/ns/activitystreams#Public']

    def validate_for_platforms(self) -> dict:
        errors = {}

        for platform in self.platforms:
            validate_fn = getattr(self, f'_validate_for_{platform}', None)

            if callable(validate_fn):
                validate_fn(errors)

        return errors

    def _validate_for_bluesky(self, errors: dict) -> None:
        platform = Platform.BLUESKY.value

        if not self.content:
            errors.setdefault(platform, []).append('Content required for Bluesky')

        if self.media:
            self._validate_media(platform, errors)

    def _validate_for_mastodon(self, errors: dict) -> None:
        platform = Platform.MASTODON.value

        if not self.content:
            errors.setdefault(platform, []).append('Content required for Mastodon')

        if self.media:
            self._validate_media(platform, errors)

    def _validate_for_pixelfed(self, errors: dict) -> None:
        platform = Platform.PIXELFED.value

        if not self.media:
            errors.setdefault(platform, []).append('Media required for Pixelfed')
            return

        self._validate_media(platform, errors)

    def _validate_media(self, platform: str, errors: dict) -> None:
        for i, media in enumerate(self.media):
            if not media.url:
                errors.setdefault(platform, []).append(f'Media {i}: missing "url"')
            if not media.type:
                errors.setdefault(platform, []).append(f'Media {i}: missing "type"')
            if not media.alt:
                errors.setdefault(platform, []).append(f'Media {i}: missing "alt"')
