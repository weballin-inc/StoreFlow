"""Schemas used specifically for tblMedia `GET /media` method"""

from typing import Optional
from fastapi import Query, Depends

from app.domain.enums import MediaType
from app.repositories.enums_repo import MediaSortField
from app.api.schemas.common import CommonListQuerySchema


class MediaListQuerySchema:
    def __init__(
        self,
        # -------- identity --------
        media_id: Optional[int] = Query(
            None,
            ge=1,
            alias=MediaSortField.id.value,
            description="`ID of the tblMedia item`",
            examples=[67],
        ),

        title: Optional[str] = Query(
            None,
            alias=MediaSortField.title,
            description="`MediaTitle`",
            examples=["Witcher"],
        ),

        media_type: Optional[MediaType] = Query(
            None,
            alias=MediaSortField.media_type,
            description="`Media type field`",
            examples=["BOOK"],
        ),

        publisher: Optional[str] = Query(
            None,
            alias=MediaSortField.publisher,
            description="`Publisher or author`",
            examples=["CDPR"],
        ),

        # -------- quantity --------
        quantity: Optional[int] = Query(
            None,
            ge=0,
            alias=MediaSortField.quantity.value,
            description="`Exact quantity of copies`",
        ),

        quantity_from: Optional[int] = Query(
            None,
            ge=0,
            alias="Quantity_from",
            description="`Quantity greater or equal`",
        ),

        quantity_to: Optional[int] = Query(
            None,
            ge=0,
            alias="Quantity_to",
            description="`Quantity less or equal`",
        ),

        # -------- price --------
        price: Optional[float] = Query(
            None,
            ge=0,
            alias=MediaSortField.price.value,
            description="`Exact item price`",
        ),

        price_from: Optional[float] = Query(
            None,
            ge=0,
            alias="Price_from",
            description="`Price greater or equal`",
        ),

        price_to: Optional[float] = Query(
            None,
            ge=0,
            alias="Price_to",
            description="`Price less or equal`",
        ),

        # -------- release year --------
        release_year: Optional[int] = Query(
            None,
            ge=0,
            alias=MediaSortField.release_year.value,
            description="`Release year of the item`",
        ),

        release_year_from: Optional[int] = Query(
            None,
            ge=0,
            alias="ReleaseYear_from",
            description="`Release year greater or equal`",
        ),

        release_year_to: Optional[int] = Query(
            None,
            ge=0,
            alias="ReleaseYear_to",
            description="`Release year less or equal`",
        ),

        # -------- sorting & paging --------
        sort_by: Optional[MediaSortField] = Query(
            None,
            alias="Sort_by",
            description="`Sort by chosen field`",
            examples=["publisher"],
        ),

        common: CommonListQuerySchema = Depends()
    ):
        self.media_id = media_id
        self.title = title
        self.media_type = media_type
        self.publisher = publisher

        self.quantity = quantity
        self.quantity_from = quantity_from
        self.quantity_to = quantity_to

        self.price = price
        self.price_from = price_from
        self.price_to = price_to

        self.release_year = release_year
        self.release_year_from = release_year_from
        self.release_year_to = release_year_to

        self.sort_by = sort_by
        self.order = common.order
        self.limit = common.limit
        self.offset = common.offset