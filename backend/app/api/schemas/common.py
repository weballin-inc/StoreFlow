from pydantic import BaseModel, Field
from typing import Literal

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