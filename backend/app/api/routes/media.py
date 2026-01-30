from fastapi import APIRouter, status, Query, Path
from typing import Optional, List

from app.api.schemas import MediaCreateSchema, MediaResponseSchema
from app.domain.enums import MediaType
from app.repositories.additional_queries import MediaSortField
from app.services.services import add_media_title, get_media_by_id
from app.repositories import media_repo


router = APIRouter(prefix="/media", tags=["Media"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=MediaResponseSchema)
def create_media(payload: MediaCreateSchema):
    """
    Add new media title.
    """
    media = add_media_title(
        title=payload.title,
        media_type=payload.media_type,
        release_year=payload.release_year,
        publisher=payload.publisher,
    )

    return media


@router.get("", status_code=status.HTTP_200_OK, response_model=List[MediaResponseSchema])
def list_media(
    media_type: Optional[MediaType] = Query(None),
    publisher: Optional[str] = Query(None),
    release_year: Optional[int] = Query(None, ge=0),

    release_year_from: Optional[int] = Query(None, ge=0),
    release_year_to: Optional[int] = Query(None, ge=0),

    sort_by: Optional[MediaSortField] = Query(None),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):

    if (
        release_year_from is not None
        and release_year_to is not None
        and release_year_from > release_year_to
    ):
        from fastapi import HTTPException

        raise HTTPException(
            status_code=422,
            detail="release_year_from cannot be greater than release_year_to",
        )

    return media_repo.list_filtered(
        media_type=media_type,
        publisher=publisher,
        release_year=release_year,
        release_year_from=release_year_from,
        release_year_to=release_year_to,
        sort_by=sort_by.value if sort_by else None,
        order=order,
        limit=limit,
        offset=offset,
    )

@router.get("/{media_id}", status_code=status.HTTP_200_OK, response_model=MediaResponseSchema)
def get_media(
    media_id: int = Path(..., ge=1),
):
    return get_media_by_id(media_id)