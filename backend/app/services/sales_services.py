"""Business logic for tblSales"""

from app.domain.models import Sale
from app.api.schemas.sales import SaleCreateSchema
from app.repositories import media_repo, sales_repo
from app.domain.exceptions import (
    MediaNotFoundError,
    MediaAlreadySoldOut,
    InvalidValueError
)

def add_sale(media_id: int, amount_sold: int) -> Sale:
    if amount_sold <= 0:
        raise InvalidValueError(f"Amount to sell must be >0. You've given {amount_sold}")

    media = media_repo.get_by_id(media_id)
    if media is None:
        raise MediaNotFoundError(f"Media with ID {media_id} not found")

    success = media_repo.decrement_media_amount(media_id, amount_sold)
    if not success:
        raise MediaAlreadySoldOut(f"Not enough items in stock to sell {amount_sold}")

    return sales_repo.insert_sale(media_id, media.price)