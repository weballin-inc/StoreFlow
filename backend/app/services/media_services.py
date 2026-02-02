"""Business logic for tblMedia"""

from app.api.schemas.media import MediaUpdateSchema
from app.domain.enums import MediaType
from app.domain.exceptions import MediaAlreadyExistsError, MediaNotFoundError
from app.domain.models import Media
from app.repositories import media_repo


# ------- Create/Add/Insert Media -------
def add_media_title(
    title: str,
    media_type: MediaType,
    release_year: int,
    publisher: str,
    quantity: int,
    price: float
) -> Media:
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

    existing = media_repo.get_by_title_and_type(title, media_type)
    if existing is not None:
        raise MediaAlreadyExistsError(
            f"Media '{existing.title}' of type '{existing.media_type}' already exists. ID {existing.id}"
        )

    media = Media(
        id=None,
        title=title,
        media_type=media_type,
        release_year=release_year,
        publisher=publisher,
        quantity=quantity,
        price=price
    )

    return media_repo.create(media)


# ------- Get/Select Media -------
def get_media_by_id(media_id: int):
    """
    Returns a specific media based on ID
    """
    media = media_repo.get_by_id(media_id)

    if media is None:
        raise MediaNotFoundError(f"Media with ID {media_id} not found")

    return media


# ------- Update Media -------
def update_media(media_id: int, data: MediaUpdateSchema) -> None:
    media = media_repo.get_by_id(media_id)

    if media is None:
        raise MediaNotFoundError(f"Media with ID {media_id} not found")

    media_repo.update(
        media_id=media_id,
        title=data.title,
        release_year=data.release_year,
        publisher=data.publisher,
        price=data.price,
    )

