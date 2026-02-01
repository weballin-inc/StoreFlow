"""Data models for API communication"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

from app.domain.enums import MediaType

############################################
#   tblMedia
############################################

class MediaCreateSchema(BaseModel): 
    title: str = Field(..., min_length=1)
    media_type: MediaType
    release_year: int = Field(..., ge=0)
    publisher: str = Field(..., min_length=1)
    amount: int = Field(..., ge=0)
    price: float = Field(..., ge=0)

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
    media_type: Optional[MediaType]
    release_year: Optional[int] = Field(None, ge=0)
    publisher: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, ge=0)

# class MediaDeleteSchema(BaseModel):
#    FORBIDDEN

############################################
#   tblSales
############################################

class SaleCreateSchema(BaseModel):
    media_id: int = Field(..., ge=1)

class SaleResponseSchema(SaleCreateSchema):
    id: int
    price: float
    date: datetime

class PagedSalesResponseSchema(BaseModel):
    items: List[Dict]
    total: int
    limit: int
    offset: int

# class SaleUpdateSchema(BaseModel):
#   FORBIDDEN

# class SaleDeleteSchema(BaseModel):
#   FORBIDDEN