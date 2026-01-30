from enum import Enum


class MediaSortField(str, Enum):
    title = "Title"
    media_type = "MediaType"
    release_year = "ReleaseYear"
    publisher = "Publisher"


class CopiesSortField(str, Enum):
    copy_id = "CopyID"
    media_id = "MediaID"
    price = "Price"
    status = "Status"