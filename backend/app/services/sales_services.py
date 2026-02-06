"""
Business logic for tblSales
- `add_sale` adds a sale record of the specified item to tblSales, along with the amount of such item being sold
- `list_sales` lists filtered tblSales rows
"""

from app.api.schemas.sales_query import SalesListQuerySchema
from app.domain.exceptions import (
    MediaNotFoundError,
    MediaAlreadySoldOut,
    InvalidValueError
)
from app.domain.models import Sale
from app.repositories import media_repo, sales_repo


# ------- Create/Add/Insert Sale -------
def add_sale(media_id: int, amount_sold: int) -> Sale:
    """
    Add a record to tblSales.
    - Add/Subtract from tblMedia based on the provided amount
    - Insert a record to tblSales.
    """

    # Validate amount of items sold
    if amount_sold <= 0:
        raise InvalidValueError(f"Amount to sell must be >0. You've given {amount_sold}")

    # Check if the media record that's being sold actually exists
    media = media_repo.get_by_id(media_id)
    if media is None:
        raise MediaNotFoundError(f"Media with ID {media_id} not found")

    # Check if the media record hasn't been sold yet
    success = media_repo.arithmetics(media_id, amount_sold)
    if not success:
        raise MediaAlreadySoldOut(f"Not enough items in stock to sell {amount_sold}")

    # INSERT sale to tblSales
    for _ in range(amount_sold):
        sale = sales_repo.insert_sale(
            media_id=media_id,
            price=media.price
        )

    return sale


# ------- Read/Get/Select Sales -------
def list_sales(query: SalesListQuerySchema) -> tuple[list[Sale], int]:
    """
    Filtered list of all records in tblSales.
    """

    # Future business rules can go HERE

    # Filtered SELECT on tblSales
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