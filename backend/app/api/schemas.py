"""Data models for API communication"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

from app.domain.enums import MediaType

############################################
#   tblMediaTitles
############################################

class MediaCreateSchema(BaseModel): 
    title: str = Field(..., min_length=1)
    media_type: MediaType
    release_year: int = Field(..., ge=0)
    publisher: str = Field(..., min_length=1)

class MediaResponseSchema(MediaCreateSchema):
    id: int

    class Config:
        from_attributes = True

class PagedMediaResponseSchema(BaseModel):
    items: List[MediaResponseSchema]
    total: int
    limit: int
    offset: int

class MediaUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    release_year: Optional[int] = Field(None, ge=0)
    publisher: Optional[str] = Field(None, min_length=1)

############################################
#   tblSales
############################################

class SaleCreateSchema(BaseModel):
    copy_id: int = Field(..., ge=1)

class SaleResponseSchema(SaleCreateSchema):
    id: int
    price: float

class PagedSalesResponseSchema(BaseModel):
    items: List[Dict]
    total: int
    limit: int
    offset: int