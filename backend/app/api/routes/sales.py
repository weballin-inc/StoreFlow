from fastapi import APIRouter, status, Depends

from app.services.sales_services import add_sale, list_sales
from app.api.schemas.sales import (
    SaleCreateSchema,
    SaleResponseSchema,
    PagedSaleResponseSchema
)
from app.api.schemas.sales_query import SalesListQuerySchema
from app.api.validators import (
    ranges,
    pagination
)


router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/{media_id}", status_code=status.HTTP_201_CREATED, response_model=SaleResponseSchema)
def create_sale(media_id: int, payload: SaleCreateSchema):

    sale = add_sale(media_id, payload.amount_sold)

    return {
        "id": sale.id,
        "media_id": sale.media_id,
        "price": sale.price,
        "date": sale.date,
        "amount_sold": payload.amount_sold,
    }


@router.get("", status_code=status.HTTP_200_OK, response_model=PagedSaleResponseSchema)
def get_sales(query: SalesListQuerySchema = Depends()):
    """
    Lists all tblSales records.
    Can be filtred by all columns.
    For Price, Date you can also provide range.
    Query can also be sorted, ordered and limited.
    """

    ranges.validate_range("price", query.price_from, query.price_to)
    ranges.validate_range("date", query.date_from, query.date_to)

    pagination.validate_pagination(query.limit, query.offset)

    items, total = list_sales(query)

    return {
        "items": items,
        "total": total,
        "limit": query.limit,
        "offset": query.offset,
    }