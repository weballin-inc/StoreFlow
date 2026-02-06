"""Definition of validators related to pagination of the select query results"""

from fastapi import HTTPException

def validate_pagination(limit: int, offset: int):
    if limit <= 0:
        raise HTTPException(422, detail="limit must be > 0")
    if offset < 0:
        raise HTTPException(422, detail="offset must be >= 0")