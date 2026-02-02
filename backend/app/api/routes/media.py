from fastapi import APIRouter, status, Query, Path, Body, Depends
from typing import Optional, List

from app.api.schemas.media import (
    MediaCreateSchema,
    MediaResponseSchema,
    MediaUpdateSchema,
    PagedMediaResponseSchema,
    MediaBatchResultSchema
)

from app.api.schemas.media_query import MediaListQuerySchema

from app.services.media_services import (
    add_media_title,
    get_media_by_id,
    update_media
)
from app.api.validators import (
    ranges,
    pagination,
    # sorting
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

    All fields are required:
    - `title`: Title of the item.
    - `media_type`: Type of the media must be within `'BOOK', 'GAME', 'MOVIE'`
    - `release_year`: Must be `>0`
    - `publisher`: Publisher/Author of the item.
    - `quantity`: Must be `>=0`
    - `price`: Must be `>0`

    The `Title` + `MediaType` combo is **unique**.

    You can input multiple items in a list. If any item fails the insert, the rest will still be processed.

    Should any error appear, refer to the reason - upon hitting `Internal Server Error` the trace is printed out in the console.
    """

    results: list[MediaBatchResultSchema] = []

    for item in payload:
        try:
            media = add_media_title(
                title=item.title,
                media_type=item.media_type,
                release_year=item.release_year,
                publisher=item.publisher,
                quantity=item.quantity,
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
            import traceback
            traceback.print_exc()

    return results


@router.get("", status_code=status.HTTP_200_OK, response_model=PagedMediaResponseSchema)
def list_media(query: MediaListQuerySchema = Depends()):
    """
    Lists all tblMedia records.
    Can be filtered by all columns.
    For ReleaseYear, Quantity and Price you can also provide range.
    Query can also be sorted, ordered and limited.
    """

    ranges.validate_range("release_year", query.release_year_from, query.release_year_to)
    ranges.validate_range("quantity", query.quantity_from, query.quantity_to)
    ranges.validate_range("price", query.price_from, query.price_to)

    pagination.validate_pagination(query.limit, query.offset)

    # sorting.validate_sorting(query.sort_by, query.order)

    items, total = media_repo.list_filtered(**query.__dict__)

    return {
        "items": items,
        "total": total,
        "limit": query.limit,
        "offset": query.offset,
    }

# @router.get("/{media_id}", status_code=status.HTTP_200_OK, response_model=MediaResponseSchema)
# def get_media(
#     media_id: int = Path(..., ge=1),
# ):
#     return get_media_by_id(media_id)


@router.put("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_media_route(
    media_id: int = Path(..., ge=1),
    payload: MediaUpdateSchema = Body(...),
):
    update_media(media_id, payload)