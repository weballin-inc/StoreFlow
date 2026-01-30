from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import MediaAlreadyExistsError, MediaNotFoundError
from app.domain.exceptions import CopyAlreadySoldError, CopyNotFoundError


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


def media_not_found_handler(request, exc: MediaNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "MEDIA_NOT_FOUND",
            "message": str(exc),
        },
    )


def copy_not_found_handler(request, exc: CopyNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "COPY_NOT_FOUND",
            "message": str(exc)},
    )


def copy_already_sold_handler(request, exc: CopyAlreadySoldError):
    return JSONResponse(
        status_code=409,
        content={
            "error": "COPY_ALREADY_SOLD",
            "message": str(exc)},
    )
