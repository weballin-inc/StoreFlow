"""Business logic for tblSales"""

from app.domain.models import Sale
from app.repositories import media_repo, sales_repo
from app.domain.exceptions import (
    MediaNotFoundError,
    MediaAlreadySoldOut,
    InvalidValueError
)
from app.api.schemas.sales_query import SalesListQuerySchema


# ------- Create/Add/Insert Sale -------
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


# ------- Read/Get/Select Sales -------
def list_sales(query: SalesListQuerySchema) -> tuple[list[Sale], int]:
    # reserved space for future business rules

    return sales_repo.list_filtered(
        sale_id=query.sale_id,
        media_id=query.media_id,

        price=query.price,
        price_from=query.price_from,
        price_to=query.price_to,

        date=query.date,
        date_from=query.date_from,
        date_to=query.date_to,

        sort_by=query.sort_by.value if query.sort_by else None,
        order=query.order,
        limit=query.limit,
        offset=query.offset,
    )