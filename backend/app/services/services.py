""" Business Logic for all operations """

from app.api.schemas import MediaUpdateSchema
from app.core.database import get_connection
from app.domain.enums import MediaType
from app.domain.exceptions import MediaAlreadyExistsError, MediaNotFoundError
from app.domain.models import Media, Sale
from app.repositories import media_repo, sales_repo


############################################
#   tblMedia
############################################

def add_media_title(
    title: str,
    media_type: MediaType,
    release_year: int,
    publisher: str,
    amount: int,
    price: float
) -> Media:
    """
    Create a new tblMedia record

    Constraints:
    - Title MUST be provided
    - MediaType MUST be in {'BOOK', 'GAME', 'MOVIE'}
    - ReleaseYear MUST be >0
    - Publisher MUST be provided
    - Amount must be >=0
    - Price must be >0

    Title+MediaType must be unique
    """

    existing = media_repo.get_by_title_and_type(title, media_type)
    if existing is not None:
        raise MediaAlreadyExistsError(
            f"Media '{Media.title}' of type '{Media.media_type.value}' already exists. ID {Media.id}"
        )

    media = Media(
        id=None,
        title=title,
        media_type=media_type,
        release_year=release_year,
        publisher=publisher,
        amount=amount,
        price=price
    )

    return media_repo.create(media)


def get_media_by_id(media_id: int):
    """
    Returns a specific media based on ID
    """
    media = media_repo.get_by_id(media_id)

    if media is None:
        raise MediaNotFoundError(f"Media with ID {media_id} not found")

    return media


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


############################################
#   tblSales
############################################
# def sell_copy(copy_id: int) -> Sale:
#     conn = get_connection()

#     try:
#         conn.execute("BEGIN")

#         copy = copies_repo.get_by_id(copy_id)
#         if copy is None:
#             raise CopyNotFoundError(f"Copy with ID {copy_id} not found")

#         if copy.status == CopyStatus.SOLD:
#             raise CopyAlreadySoldError(f"Copy with ID {copy_id} already sold")

#         sale = Sale(
#             id=copy.id,
#             copy_id=copy_id,
#             price=copy.price,
#         )

#         created_sale = sales_repo.create_with_conn(conn, sale)

#         copies_repo.update_status_with_conn(conn, sale.id, CopyStatus.SOLD)

#         conn.commit()
#         return created_sale

#     except:
#         conn.rollback()
#         raise

#     finally:
#         conn.close()

