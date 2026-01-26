from fastapi import APIRouter, status, Query
from typing import Optional, List

from app.api.schemas import MediaCreateSchema, MediaResponseSchema
from app.domain.enums import MediaType
from app.services.services import add_media_title
from app.services.services import get_all_media_titles
from app.repositories import media_repo


router = APIRouter(prefix="/media", tags=["Media"])


@router.post("",status_code=status.HTTP_201_CREATED,response_model=MediaResponseSchema)
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


@router.get("", status_code=status.HTTP_200_OK, response_model=list[MediaResponseSchema])
def list_media(
    media_type: Optional[MediaType] = Query(None),
    publisher: Optional[str] = Query(None),
    release_year: Optional[int] = Query(None, ge=0),
):
    return media_repo.list_filtered(
        media_type=media_type,
        publisher=publisher,
        release_year=release_year,
    )