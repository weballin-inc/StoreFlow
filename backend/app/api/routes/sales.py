from fastapi import APIRouter, status
from app.api.schemas import SaleCreateSchema, SaleResponseSchema
from app.services.services import sell_copy

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=SaleResponseSchema)
def create_sale(payload: SaleCreateSchema):
    return sell_copy(payload.copy_id)
