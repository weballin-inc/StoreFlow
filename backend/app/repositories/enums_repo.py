from enum import Enum

class MediaSortField(str, Enum):
    title = "Title"
    media_type = "MediaType"
    release_year = "ReleaseYear"
    publisher = "Publisher"


class SalesSortField(str, Enum):
    sale_id = "s.SaleID"
    sale_price = "s.Price"
    copy_id = "c.CopyID"
    media_id = "m.MediaID"
    title = "m.Title"
    release_year = "m.ReleaseYear"