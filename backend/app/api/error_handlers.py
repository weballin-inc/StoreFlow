"""
```
@app.exception_handler(CopyNotAvailableError)
async def handle_copy_error(request, exc):
    return JSONResponse(status_code=400, content={"error": "Copy not available"})
```
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import MediaAlreadyExistsError


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(MediaAlreadyExistsError)
    async def media_already_exists_handler(
        request: Request,
        exc: MediaAlreadyExistsError,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "MEDIA_ALREADY_EXISTS",
                "message": str(exc),
            },
        )