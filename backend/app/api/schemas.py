"""Data models for API communication"""
from pydantic import BaseModel, Field

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


class CopyCreateSchema(BaseModel):
    media_id: int = Field(..., ge=1)
    price: float = Field(..., ge=0)


class CopyResponseSchema(BaseModel):
    id: int
    media_id: int
    price: float
    status: CopyStatus