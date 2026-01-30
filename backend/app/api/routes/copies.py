from fastapi import APIRouter, status

from app.api.schemas import CopyCreateSchema, CopyResponseSchema
from app.services.services import add_copy


router = APIRouter(prefix="/copies",tags=["Copies"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CopyResponseSchema)
def create_copy(payload: CopyCreateSchema):
    return add_copy(
        media_id=payload.media_id,
        price=payload.price
    )