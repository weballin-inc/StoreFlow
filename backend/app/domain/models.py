from dataclasses import dataclass
from typing import Optional

from app.domain.enums import MediaType


@dataclass
class MediaTitle:
    id: Optional[int]
    title: str
    media_type: MediaType
    release_year: Optional[int] = None
    publisher: Optional[str] = None