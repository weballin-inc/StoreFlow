from fastapi import APIRouter, status, Path, Query, HTTPException
from typing import List, Optional

from app.api.schemas import CopyCreateSchema, CopyResponseSchema
from app.domain.enums import CopyStatus
from app.services.services import add_copy
from app.repositories import copies_repo
from app.repositories.additional_queries import CopiesSortField


router = APIRouter(prefix="/copies",tags=["Copies"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CopyResponseSchema)
def create_copy(payload: CopyCreateSchema):
    return add_copy(
        media_id=payload.media_id,
        price=payload.price
    )


@router.get("", status_code=status.HTTP_200_OK, response_model=List[CopyResponseSchema])
def list_copies(
    copy_id: Optional[int] = Query(None, ge=1),
    media_id: Optional[int] = Query(None, ge=1),
    price: Optional[float] = Query(None, ge=0),
    status: Optional[CopyStatus] = Query(None),
    sort_by: Optional[CopiesSortField] = Query(None),
    order: str = Query("asc", patter="^(asc|desc)$"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    ):
    return copies_repo.list_filtered(
        copy_id=copy_id,
        media_id=media_id,
        price=price,
        status=status,
        sort_by=sort_by.value if sort_by else None,
        order=order,
        limit=limit,
        offset=offset,
    )

@router.get("/{copy_id}", status_code=status.HTTP_200_OK, response_model=CopyResponseSchema)
def get_copy(
    copy_id: int = Path(..., ge=1)
):
    copy = copies_repo.get_by_id(copy_id)

    if copy is None:
        raise HTTPException(
            status_code=404,
            detail="Copy not found"
        )

    return copy
