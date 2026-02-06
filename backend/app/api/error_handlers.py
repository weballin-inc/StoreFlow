

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    InvalidKeyError,
    InvalidValueError,
    MediaAlreadyExistsError,
    MediaNotFoundError,
    MediaAlreadySoldOut
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


def media_already_sold_out(
    request: Request,
    exc: MediaAlreadySoldOut,
):
    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        content={
            "error": "MEDIA_ALREADY_SOLD_OUT",
            "message": str(exc),
        },
    )

def invalid_value_error(
    request: Request,
    exc: InvalidValueError
):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": "INVALID_VALUE_ERROR",
            "message": str(exc)
        },
    )


def invalid_key_error(
    request: Request,
    exc: InvalidKeyError
):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": "INVALID_KEY_ERROR",
            "message": str(exc)
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

    app.add_exception_handler(
        MediaAlreadySoldOut,
        media_already_sold_out,
    )

    app.add_exception_handler(
        InvalidValueError,
        invalid_value_error
    )

    app.add_exception_handler(
        InvalidKeyError,
        invalid_key_error
    )