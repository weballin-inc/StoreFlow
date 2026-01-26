"""
    Modele danych do komunikacji przez API
"""

from typing import Optional
from pydantic import BaseModel, Field

from app.domain.enums import MediaType


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