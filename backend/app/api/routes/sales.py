from fastapi import APIRouter, status

from app.api.schemas.sales import (
    SaleCreateSchema,
    SaleResponseSchema,
    PagedSalesResponseSchema
)
from app.services import sales_services


router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/{media_id}", status_code=status.HTTP_201_CREATED, response_model=SaleResponseSchema)
def create_sale(media_id: int, payload: SaleCreateSchema):

    sale = sales_services.add_sale(
        media_id,
        payload.amount_sold
    )

    return {
        "id": sale.id,
        "media_id": sale.media_id,
        "price": sale.price,
        "date": sale.date,
        "amount_sold": payload.amount_sold,
    }