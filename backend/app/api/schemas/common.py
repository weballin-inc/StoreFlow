from fastapi import Query
from pydantic import BaseModel, Field
from typing import Literal, Optional

class CommonListQuerySchema:
    def __init__(
        self,
        # -------- sorting & paging --------
        sort_by: Optional[str] = Query(
            None,
            alias="Sort_by",
            description="`Sort by chosen field`",
            examples=["publisher"],
        ),

        order: str = Query(
            "asc",
            alias="Order",
            pattern="^(asc|desc)$",
            description="`Sort order: ascending or descending`",
        ),

        limit: int = Query(
            20,
            ge=1,
            le=100,
            alias="Limit",
            description="`Maximum number of rows`",
        ),

        offset: int = Query(
            0,
            ge=0,
            alias="Offset",
            description="`Starting row offset`",
        )        
    ):
        self.sort_by = sort_by
        self.order = order
        self.limit = limit
        self.offset = offset


class PaginationMeta(BaseModel):
    total: int
    limit: int
    offset: int


class IncrementSchema(BaseModel):
    delta: Literal[1, -1] = Field(
        ...,
        description="Use +1 to increase, -1 to decrease."
    )

    class Config:
        extra = "forbid"