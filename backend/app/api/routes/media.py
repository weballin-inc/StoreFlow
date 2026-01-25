from fastapi import APIRouter, status
from typing import List

from app.api.schemas import MediaCreateSchema, MediaResponseSchema
from app.services.services import add_media_title
from app.services.services import get_all_media_titles


router = APIRouter(
    prefix="/media",
    tags=["Media"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=MediaResponseSchema,
)
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


@router.get(
    "",
    response_model=list[MediaResponseSchema],
)
def get_all_media():
    """
    Get all media titles.
    """
    return get_all_media_titles()
