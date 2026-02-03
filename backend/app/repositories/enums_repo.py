from enum import Enum

class MediaSortField(str, Enum):
    id = "MediaID"
    title = "Title"
    media_type = "MediaType"
    release_year = "ReleaseYear"
    publisher = "Publisher"
    quantity = "Quantity"
    price = "Price"


class SalesSortField(str, Enum):
    sale_id = "s.SaleID"
    media_id = "m.MediaID"
    sale_price = "s.Price"
    sale_date = "s.Date"
