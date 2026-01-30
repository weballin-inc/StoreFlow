""" Business Logic for all operations """
from app.domain.models import MediaTitle, MediaCopy, Sale
from app.domain.enums import MediaType, CopyStatus
from app.domain.exceptions import MediaAlreadyExistsError, MediaNotFoundError
from app.domain.exceptions import CopyAlreadySoldError, CopyNotFoundError
from app.repositories import media_repo, copies_repo, sales_repo


############################################
#   tblMediaTitles
############################################

def add_media_title(
    title: str,
    media_type: MediaType,
    release_year: int,
    publisher: str,
) -> MediaTitle:
    """
    Business procedure:
    - media title must be unique per (title, media_type)
    """

    existing = media_repo.get_by_title_and_type(title, media_type)
    if existing is not None:
        raise MediaAlreadyExistsError(
            f"Media '{title}' of type '{media_type.value}' already exists."
        )

    media = MediaTitle(
        id=None,
        title=title,
        media_type=media_type,
        release_year=release_year,
        publisher=publisher,
    )

    return media_repo.create(media)


def get_media_by_id(media_id: int):
    """
    Returns a specific media based on ID
    """
    media = media_repo.get_by_id(media_id)

    if media is None:
        raise MediaNotFoundError(f"Media with ID{media_id} not found")

    return media


############################################
#   tblMediaCopies
############################################

def add_copy(media_id: int, price: float) -> MediaCopy:
    media = media_repo.get_by_id(media_id)

    if media is None:
        raise MediaNotFoundError(f"Media with ID{media_id} not found")

    copy = MediaCopy(
        id=None,
        media_id=media_id,
        price=price,
        status=CopyStatus.AVAILABLE
    )

    return copies_repo.create(copy)


############################################
#   tblSales
############################################
def sell_copy(copy_id: int) -> Sale:
    copy = copies_repo.get_by_id(copy_id)

    if copy is None:
        raise CopyNotFoundError(f"Copy with id {copy_id} not found")

    if copy.status == CopyStatus.SOLD:
        raise CopyAlreadySoldError(f"Copy {copy_id} already sold")

    sale = Sale(
        id=None,
        copy_id=copy_id,
        price=copy.price,
    )

    created_sale = sales_repo.create(sale)

    copies_repo.update_status(copy_id, CopyStatus.SOLD)

    return created_sale