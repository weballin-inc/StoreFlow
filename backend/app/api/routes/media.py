from fastapi import APIRouter, status, Query, Path, Body, Depends
from typing import Optional, List, Literal

from app.api.schemas.media import (
    MediaCreateSchema,
    MediaResponseSchema,
    MediaUpdateSchema,
    PagedMediaResponseSchema,
    MediaBatchResultSchema
)
from app.api.schemas.media_query import MediaListQuerySchema
from app.api.schemas.common import IncrementSchema

from app.services.media_services import (
    add_media_title,
    list_media,
    update_media_by_id,
    patch_media_counter_by_id
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
            media = add_media_title(item)

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
                    err_reason=f"{str(e)}"
                )
            )

        except Exception as e:
            results.append(
                MediaBatchResultSchema(
                    title=item.title,
                    status="FAIL",
                    err_reason=f"Internal Server Error: {str(e)}"
                )
            )
            import traceback
            traceback.print_exc()

    return results


@router.get("", status_code=status.HTTP_200_OK, response_model=PagedMediaResponseSchema)
def get_media(query: MediaListQuerySchema = Depends()):
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

    items, total = list_media(query)

    return {
        "items": items,
        "total": total,
        "limit": query.limit,
        "offset": query.offset,
    }


@router.put("/{media_id}", status_code=status.HTTP_200_OK, response_model=MediaResponseSchema)
def put_media(media_id: int, payload: MediaUpdateSchema):
    """
    Edit specific record based on MediaID
    You can use it to edit single or multiple fields.

    Allowed fields:
    - `title`: Title
    - `media_type`: MediaType, but must be unique with Title+MediaType
    - `release_year`: ReleaseYear
    - `publisher`: Publisher
    - `quantity`: Quantity, must be >=0
    - `price`: Price, must be >= 0
    """

    media = update_media_by_id(
        media_id=media_id,
        data=payload
    )

    return media


@router.patch("/{media_id}/{field}", status_code=status.HTTP_200_OK, response_model=MediaResponseSchema)
def patch_media_counter(
    media_id: int,
    field: Literal["quantity", "price"],
    payload: IncrementSchema
):
    media = patch_media_counter_by_id(
        media_id=media_id,
        field=field,
        delta=payload.delta,
    )
    return media