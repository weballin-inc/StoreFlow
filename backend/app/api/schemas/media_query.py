from typing import Optional
from pydantic import BaseModel
from fastapi import Query

from app.domain.enums import MediaType
from app.repositories.enums_repo import MediaSortField


class MediaListQuerySchema(BaseModel):
    # -------- identity --------
    media_id: Optional[int] = Query(
        None,
        ge=1,
        alias=MediaSortField.id,
        description="ID of the tblMedia item",
        examples=[67],
    )

    title: Optional[str] = Query(
        None,
        alias=MediaSortField.title,
        description="MediaTitle",
        examples=["Witcher"],
    )

    media_type: Optional[MediaType] = Query(
        None,
        alias=MediaSortField.media_type,
        description="Media type field",
        examples=["BOOK"],
    )

    publisher: Optional[str] = Query(
        None,
        alias=MediaSortField.publisher,
        description="Publisher or author",
        examples=["CDPR"],
    )

    # -------- quantity --------
    quantity: Optional[int] = Query(
        None,
        ge=0,
        alias=MediaSortField.quantity,
        description="Exact quantity of copies",
    )

    quantity_from: Optional[int] = Query(
        None,
        ge=0,
        alias="Quantity_from",
        description="Quantity greater or equal",
    )

    quantity_to: Optional[int] = Query(
        None,
        ge=0,
        alias="Quantity_to",
        description="Quantity less or equal",
    )

    # -------- price --------
    price: Optional[float] = Query(
        None,
        ge=0,
        alias=MediaSortField.price,
        description="Exact item price",
    )

    price_from: Optional[float] = Query(
        None,
        ge=0,
        alias="Price_from",
        description="Price greater or equal",
    )

    price_to: Optional[float] = Query(
        None,
        ge=0,
        alias="Price_to",
        description="Price less or equal",
    )

    # -------- release year --------
    release_year: Optional[int] = Query(
        None,
        ge=0,
        alias=MediaSortField.release_year,
        description="Release year of the item",
    )

    release_year_from: Optional[int] = Query(
        None,
        ge=0,
        alias="ReleaseYear_from",
        description="Release year greater or equal",
    )

    release_year_to: Optional[int] = Query(
        None,
        ge=0,
        alias="ReleaseYear_to",
        description="Release year less or equal",
    )

    # -------- sorting & paging --------
    sort_by: Optional[MediaSortField] = Query(
        None,
        alias="Sort_by",
        description="Sort by chosen field",
        examples=["publisher"],
    )

    order: str = Query(
        "asc",
        alias="Order",
        pattern="^(asc|desc)$",
        description="Sort order: ascending or descending",
    )

    limit: int = Query(
        20,
        ge=1,
        le=100,
        alias="Limit",
        description="Maximum number of rows",
    )

    offset: int = Query(
        0,
        ge=0,
        alias="Offset",
        description="Starting row offset",
    )
