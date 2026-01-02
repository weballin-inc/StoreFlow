"""
Stale i stany
- status egzemplarza
- status pracownika

np. zamiast
    if status == "sold":

    if status == CopyStatus.SOLD

Tylko definicje stanow i typow, bez logiki.

Przyklad:
```
    from enum import Enum

    class CopyStatus(Enum):
        AVAILABLE = "available"
        SOLD = "sold"

    class EmployeeStatus(Enum):
        ACTIVE = "active"
        INACTIVE = "inactive"

    class MediaType(Enum):
        BOOK = "book"
        MOVIE = "movie"
        GAME = "game"
```
"""