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
    copy_id: int
    price: float
    date: datetime


