from fastapi import APIRouter, status, Query, Path, HTTPException
from typing import Optional, List, Dict

from app.api.schemas import SaleCreateSchema, SaleResponseSchema
from app.services.services import sell_copy
from app.repositories import sales_repo
from app.repositories.additional_queries import SalesSortField

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=SaleResponseSchema)
def create_sale(payload: SaleCreateSchema):
    return sell_copy(payload.copy_id)


@router.get("", status_code=status.HTTP_200_OK, response_model=List[Dict])
def list_sales(
    media_type: Optional[str] = Query(None), 
    publisher: Optional[str] = Query(None),
    release_year_from: Optional[int] = Query(None, ge=0),
    release_year_to: Optional[int] = Query(None, ge=0),
    sort_by: Optional[SalesSortField] = Query(None),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return sales_repo.list_filtered(
        media_type=media_type,
        publisher=publisher,
        release_year_from=release_year_from,
        release_year_to=release_year_to,
        sort_by=sort_by.value if sort_by else None,
        order=order,
        limit=limit,
        offset=offset,
    )

@router.get("/{sale_id}", status_code=status.HTTP_200_OK, response_model=SaleResponseSchema)
def get_sale(
    sale_id: int = Path(..., ge=1)
):
    sale = sales_repo.get_by_id(sale_id)

    if sale is None:
        raise HTTPException(
            status_code=404,
            detail="Sale record not found"
        )

    return sale