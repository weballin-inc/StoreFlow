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


class SalesSortField(str, Enum):
    sale_id = "s.SaleID"
    sale_price = "s.Price"
    copy_id = "c.CopyID"
    media_id = "m.MediaID"
    title = "m.Title"
    release_year = "m.ReleaseYear"