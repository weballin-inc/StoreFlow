"""Data models for API communication"""
from pydantic import BaseModel, Field
from typing import List, Dict

from app.domain.enums import MediaType, CopyStatus


class MediaCreateSchema(BaseModel): 
    title: str = Field(..., min_length=1)
    media_type: MediaType
    release_year: int = Field(..., ge=0)
    publisher: str = Field(..., min_length=1)

class MediaResponseSchema(BaseModel):
    id: int
    title: str
    media_type: MediaType
    release_year: int
    publisher: str

    class Config:
        from_attributes = True

class PagedMediaResponseSchema(BaseModel):
    items: List[MediaResponseSchema]
    total: int
    limit: int
    offset: int


class CopyCreateSchema(BaseModel):
    media_id: int = Field(..., ge=1)
    price: float = Field(..., ge=0)

class CopyResponseSchema(BaseModel):
    id: int
    media_id: int
    price: float
    status: CopyStatus

class PagedCopiesResponseSchema(BaseModel):
    items: List[CopyResponseSchema]
    total: int
    limit: int
    offset: int


class SaleCreateSchema(BaseModel):
    copy_id: int = Field(..., ge=1)

class SaleResponseSchema(BaseModel):
    id: int
    copy_id: int
    price: float

class PagedSalesResponseSchema(BaseModel):
    items: List[Dict]
    total: int
    limit: int
    offset: int