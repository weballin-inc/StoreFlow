from dataclasses import dataclass
from typing import Optional

from app.domain.enums import MediaType, CopyStatus


@dataclass
class MediaTitle:
    id: Optional[int]
    title: str
    media_type: MediaType
    release_year: int
    publisher: str


@dataclass
class MediaCopy:
    id: Optional[int]
    media_id: int
    price: float
    status: CopyStatus