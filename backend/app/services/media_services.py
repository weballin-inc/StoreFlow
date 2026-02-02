"""Business logic for tblMedia"""
from typing import Literal

from app.api.schemas.media import MediaCreateSchema, MediaUpdateSchema
from app.domain.enums import MediaType
from app.domain.exceptions import (
    InvalidKeyError,
    InvalidValueError,
    MediaAlreadyExistsError,
    MediaNotFoundError
)
from app.domain.models import Media
from app.repositories import media_repo


# ------- Create/Add/Insert Media -------
def add_media_title(data: MediaCreateSchema) -> Media:
    """
    Create a new tblMedia record

    Constraints:
    - Title MUST be provided
    - MediaType MUST be in {'BOOK', 'GAME', 'MOVIE'}
    - ReleaseYear MUST be >0
    - Publisher MUST be provided
    - quantity must be >=0
    - Price must be >0

    Title+MediaType must be unique
    """

    existing = media_repo.get_by_title_and_type(data.title, data.media_type)
    if existing is not None:
        raise MediaAlreadyExistsError(
            f"Media '{existing.title}' of type '{existing.media_type}' already exists. ID {existing.id}"
        )

    if data.price is not None and data.price < 0:
        raise InvalidValueError(f"Price cannot be less than 0. You've given '{data.price}'")

    media = Media(
        id=None,
        title=data.title,
        media_type=data.media_type,
        release_year=data.release_year,
        publisher=data.publisher,
        quantity=data.quantity,
        price=data.price
    )

    return media_repo.create(media)


# ------- Update Media -------
def update_media_by_id(
    media_id: int,
    data: MediaUpdateSchema,
) -> Media:

    # --- get existing ---
    existing = media_repo.get_by_id(media_id)
    if existing is None:
        raise MediaNotFoundError(f"Media with ID {media_id} not found")

    # --- Title + MediaType uniqueness ---
    new_title = (data.title if data.title is not None else existing.title)
    new_media_type = (data.media_type if data.media_type is not None else existing.media_type)

    conflict = media_repo.get_by_title_and_type(new_title, new_media_type)
    if conflict is not None and conflict.id != media_id:
        raise MediaAlreadyExistsError(
            f"Media '{new_title}' of type '{new_media_type.value}' already exists at ID {conflict.id}."
        )

    # --- apply updates ---
    updated = Media(
        id=media_id,
        title=new_title,
        media_type=new_media_type,
        release_year=(data.release_year if data.release_year is not None else existing.release_year),
        publisher=(data.publisher if data.publisher is not None else existing.publisher),
        quantity=(data.quantity if data.quantity is not None else existing.quantity),
        price=(data.price if data.price is not None else existing.price),
    )

    return media_repo.update(updated)


def patch_media_counter_by_id(
    media_id: int,
    field: Literal["quantity", "price"],
    delta: int,
) -> Media:

    media = media_repo.get_by_id(media_id)
    if media is None:
        raise MediaNotFoundError(f"Media with ID {media_id} not found")

    if field == "quantity":
        new_value = media.quantity + delta
        if new_value < 0:
            raise InvalidValueError("Quantity cannot be negative")

        media.quantity = new_value

    elif field == "price":
        new_value = media.price + delta
        if new_value < 0:
            raise InvalidValueError("Price cannot be negative")

        media.price = new_value

    else:
        raise InvalidKeyError("Invalid field")

    return media_repo.update(media)
