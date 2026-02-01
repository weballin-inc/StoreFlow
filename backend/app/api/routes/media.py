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
    - quantity must be `>=0`
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
def list_media(
    media_id: Optional[int] = Query(None, ge=1, alias="Media ID", description="`ID of the tblMedia item`", examples="67"),
    media_type: Optional[MediaType] = Query(None, alias="Media Type", description="`Media type field`", examples="BOOK"),
    publisher: Optional[str] = Query(None, alias="Publisher/Author", description="`Publisher or Author field`", examples="CDPR"),

    quantity: Optional[int] = Query(None, ge=0, alias="Quantity", description="`Quantity of item copies`", examples="420"),
    quantity_from: Optional[int] = Query(None, ge=0, alias="Quantity from", description="`Greater or equal`", examples="1"),
    quantity_to: Optional[int] = Query(None, ge=0, alias="Quantity to", description="`Less or equal`", examples="420"),

    price: Optional[float] = Query(None, ge=0, alias="Price", description="`Price of the item`", examples="21.37"),
    price_from: Optional[float] = Query(None, ge=0, alias="Price from", description="`Greater or equal`", examples="0.01"),
    price_to: Optional[float] = Query(None, ge=0, alias="Price to", description="`Less or equal`", examples="21.37"),

    release_year: Optional[int] = Query(None, ge=0, alias="Release Year", description="`Release year of the item`", examples="2015"),
    release_year_from: Optional[int] = Query(None, ge=0, alias="Release Year from", description="`Greater or equal`", examples="1987"),
    release_year_to: Optional[int] = Query(None, ge=0, alias="Release Year to", description="`Less or equal`", examples="2020"),
    
    sort_by: Optional[MediaSortField] = Query(None, alias="Sort by", description="`Sort by chosen field`", examples="`publisher`"),
    order: str = Query("asc", pattern="asc/desc", alias="Order", description="`Order by the chosen field either (asc)ending or (desc)ending.`", examples="desc"),
    limit: int = Query(20, ge=1, le=100, alias="Limit", description="`Limit the query results to a specified number of rows`", examples="10"),
    offset: int = Query(0, ge=0, alias="Offset", description="`Start showing results from specific row`", examples="2"),
):
    """
    Lists all tblMedia records.
    Can be filtered by all columns.
    For ReleaseYear, quantity, Price you can also provide range.
    Query can also be sorted, ordered and limited.
    """

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