from enum import Enum

class MediaType(str, Enum):
    BOOK = "BOOK"
    GAME = "GAME"
    MOVIE = "MOVIE"

class CopyStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    SOLD = "SOLD"