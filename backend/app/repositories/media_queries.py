from enum import Enum


class MediaSortField(str, Enum):
    title = "MediaTitle"
    media_type = "MediaType"
    release_year = "MediaReleaseYear"
    publisher = "MediaPublisher"