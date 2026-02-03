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
    id = "SaleID"
    media_id = "MediaID"
    price = "Price"
    date = "Date"
