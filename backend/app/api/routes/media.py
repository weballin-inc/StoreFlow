import traceback
from fastapi import APIRouter, status, Query, Path, Body
from typing import Optional, List

from app.api.schemas import (
    MediaCreateSchema,
    MediaResponseSchema,
    MediaUpdateSchema,
    PagedMediaResponseSchema,
    MediaBatchResultSchema
)
from app.services.services import (
    add_media_title,
    get_media_by_id,
    update_media
)
from app.domain.exceptions import MediaAlreadyExistsError
from app.domain.enums import MediaType
from app.repositories.enums_repo import MediaSortField
from app.repositories import media_repo


router = APIRouter(prefix="/media", tags=["Media"])


@router.post("", status_code=status.HTTP_200_OK, response_model=List[MediaBatchResultSchema])
def create_media(payload: List[MediaCreateSchema]):
    """
    Create (multiple) media records with specified columns
    Constraints:
    - Title MUST be provided
    - MediaType MUST be in `{'BOOK', 'GAME', 'MOVIE'}`
    - ReleaseYear MUST be `>0`
    - Publisher MUST be provided
    - Amount must be `>=0`
    - Price must be `>0`
    """

    results: list[MediaBatchResultSchema] = []

    for item in payload:
        try:
            media = add_media_title(
                title=item.title,
                media_type=item.media_type,
                release_year=item.release_year,
                publisher=item.publisher,
                amount=item.amount,
                price=item.price
            )

            results.append(
                MediaBatchResultSchema(
                    id=media.id,
                    title=item.title,
                    status="SUCCESS"
                )
            )

        except MediaAlreadyExistsError as e:
            results.append(
                MediaBatchResultSchema(
                    title=item.title,
                    status="FAIL",
                    reason=f"{str(e)}"
                )
            )

        except Exception as e:
            results.append(
                MediaBatchResultSchema(
                    title=item.title,
                    status="FAIL",
                    reason=f"Internal Server Error: {str(e)}"
                )
            )
            traceback.print_exc()

    return results


@router.get("", status_code=status.HTTP_200_OK, response_model=PagedMediaResponseSchema)
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

    items, total = media_repo.list_filtered(
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

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }

@router.get("/{media_id}", status_code=status.HTTP_200_OK, response_model=MediaResponseSchema)
def get_media(
    media_id: int = Path(..., ge=1),
):
    return get_media_by_id(media_id)


@router.put("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_media_route(
    media_id: int = Path(..., ge=1),
    payload: MediaUpdateSchema = Body(...),
):
    update_media(media_id, payload)