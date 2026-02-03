from typing import Optional
from fastapi import Query, Depends

from app.repositories.enums_repo import SalesSortField
from app.api.schemas.common import CommonListQuerySchema

class SalesListQuerySchema:
    def __init__(
        self,
        # -------- identity --------
        sale_id: Optional[int] = Query(
            None,
            ge=1,
            alias=SalesSortField.id.value,
            description="`ID of the tblSales item`",
            examples=[69],
        ),

        media_id: Optional[int] = Query(
            None,
            ge=1,
            alias=SalesSortField.media_id.value,
            description="`MediaID of the tblSales item`",
            examples=[2],
        ),

        # -------- price --------
        price: Optional[float] = Query(
            None,
            ge=0,
            alias=SalesSortField.price.value,
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
        date: Optional[int] = Query(
            None,
            ge=0,
            alias=SalesSortField.date.value,
            description="`Exact date of the sale`",
        ),

        date_from: Optional[int] = Query(
            None,
            ge=0,
            alias="Date_from",
            description="`Sale date greater or equal`",
        ),

        date_to: Optional[int] = Query(
            None,
            ge=0,
            alias="Date_to",
            description="`Sale date less or equal`",
        ),

        # -------- sorting & paging --------
        sort_by: Optional[SalesSortField] = Query(
            None,
            alias="Sort_by",
            description="`Sort by chosen field`",
            examples=["Price"],
        ),

        common: CommonListQuerySchema = Depends()
    ):
        self.sale_id = sale_id
        self.media_id = media_id

        self.price = price
        self.price_from = price_from
        self.price_to = price_to

        self.release_year = date
        self.release_year_from = date_from
        self.release_year_to = date_to

        self.sort_by = sort_by
        self.order = common.order
        self.limit = common.limit
        self.offset = common.offset