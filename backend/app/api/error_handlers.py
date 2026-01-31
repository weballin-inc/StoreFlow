from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    MediaAlreadyExistsError,
    MediaNotFoundError,
)

def media_already_exists_handler(
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


def media_not_found_handler(
    request: Request,
    exc: MediaNotFoundError,
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "MEDIA_NOT_FOUND",
            "message": str(exc),
        },
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        MediaAlreadyExistsError,
        media_already_exists_handler,
    )

    app.add_exception_handler(
        MediaNotFoundError,
        media_not_found_handler,
    )