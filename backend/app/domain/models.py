"""Models for tblMedia and tblSale columns. Used for structured manipulation of the database."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.enums import MediaType


@dataclass
class Media:
    id: Optional[int]
    title: str
    media_type: MediaType
    release_year: int
    publisher: str
    quantity: int
    price: float


@dataclass
class Sale:
    id: Optional[int]
    media_id: int
    price: float
    date: datetime


