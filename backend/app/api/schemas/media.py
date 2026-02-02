from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from app.domain.enums import MediaType

# ---------- Create ----------

class MediaCreateSchema(BaseModel):
    title: str = Field(..., min_length=1)
    media_type: MediaType
    release_year: int = Field(..., ge=0)
    publisher: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., ge=0)

# ---------- Update ----------

class MediaUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    media_type: Optional[MediaType] = Field(None, min_length=1)
    release_year: Optional[int] = Field(None, ge=0)
    publisher: Optional[str] = Field(None, min_length=1)
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, ge=0)

    class Config:
        extra = "forbid"

# ---------- Response ----------

class MediaResponseSchema(MediaCreateSchema):
    id: int

    class Config:
        from_attributes = True

# ---------- Batch ----------

class MediaBatchResultSchema(BaseModel):
    id: int | None = None
    title: str
    status: Literal["SUCCESS", "FAIL"]
    err_reason: str | None = None

# ---------- Paged ----------

class PagedMediaResponseSchema(BaseModel):
    items: List[MediaResponseSchema]
    total: int
    limit: int
    offset: int