"""
tblMedia CRUD operation against SQL database
- `get_by_title_and_type` searches records by Title+MediaType combo, used for validating the UNIQUE constraint
- `get_by_id` searches records by MediaID, used for validating MediaAlreadyExistsError
- `create` creates a tblMedia record
- `list_filtered` filtered search on tblMedia
- `update` updates multiple (selected) rows in tblMedia
- `arithmetics` updates countable fields in tblMedia, either by incrementing or decrementing the value.
"""

from typing import Optional

from app.core.database import get_connection
from app.domain.enums import MediaType
from app.domain.models import Media
from app.repositories.enums_repo import MediaSortField


# Used to query if inserting a potential duplicate
def get_by_title_and_type(
    title: str,
    media_type: MediaType
) -> Optional[Media]:
    """
    Returns tblMedia record if found by `Title`+`MediaType`, otherwise None.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            MediaID, Title, MediaType,
            ReleaseYear, Publisher, Quantity, Price
        FROM tblMedia
        WHERE Title = ? AND MediaType = ?
        """,
        (title, media_type.value),
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return Media(
        id=row[0],
        title=row[1],
        media_type=row[2],
        release_year=row[3],
        publisher=row[4],
        quantity=row[5],
        price=row[6]
    )


def get_by_id(media_id: int) -> Optional[Media]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MediaID, Title, MediaType, ReleaseYear, Publisher, Quantity, Price
        FROM tblMedia
        WHERE MediaID = ?
        """,
        (media_id,),
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return Media(
        id=row[0],
        title=row[1],
        media_type=MediaType(row[2]),
        release_year=row[3],
        publisher=row[4],
        quantity=row[5],
        price=row[6]
    )


# Used to insert
def create(media: Media) -> Media:
    """
    Inserts a new tblMedia record into the database and returns it with ID.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tblMedia (Title, MediaType, ReleaseYear, Publisher, Quantity, Price)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            media.title,
            media.media_type.value,
            media.release_year,
            media.publisher,
            media.quantity,
            media.price
        ),
    )

    conn.commit()
    conn.close()

    return Media(
        id=cursor.lastrowid,
        title=media.title,
        media_type=media.media_type,
        release_year=media.release_year,
        publisher=media.publisher,
        quantity=media.quantity,
        price=media.price
    )


def list_filtered(
    media_id: int | None = None,
    title: str | None = None,
    media_type: MediaType | None = None,
    publisher: str | None = None,

    quantity: int | None = None,
    quantity_from: int | None = None,
    quantity_to: int | None = None,

    price: float | None = None,
    price_from: float | None = None,
    price_to: float | None = None,

    release_year: int | None = None,
    release_year_from: int | None = None,
    release_year_to: int | None = None,

    sort_by: str | None = None,
    order: str = "asc",
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[Media], int]:
    """
    Constructs the SELECT query with filters based on the parsed parameters.
    Outputs items as tblMedia records and total amount of rows selected.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Base query
    base_query = """
        FROM tblMedia
        WHERE 1 = 1
    """

    params: list = []

    # Exact filters
    if media_id is not None:
        base_query += " AND MediaID = ?"
        params.append(media_id)

    if title is not None:
        base_query += " AND Title LIKE ?"
        params.append(f"%{title}%")

    if media_type is not None:
        base_query += " AND MediaType = ?"
        params.append(media_type.value)

    if publisher is not None:
        base_query += " AND Publisher LIKE ?"
        params.append(f"%{publisher}%")

    if quantity is not None:
        base_query += " AND Quantity = ?"
        params.append(quantity)

    if price is not None:
        base_query += " AND Price = ?"
        params.append(price)

    if release_year is not None:
        base_query += " AND ReleaseYear = ?"
        params.append(release_year)

    # Range filters
    if quantity_from is not None:
        base_query += " AND Quantity >= ?"
        params.append(quantity_from)

    if quantity_to is not None:
        base_query += " AND Quantity <= ?"
        params.append(quantity_to)

    if price_from is not None:
        base_query += " AND Price >= ?"
        params.append(price_from)

    if price_to is not None:
        base_query += " AND Price <= ?"
        params.append(price_to)

    if release_year_from is not None:
        base_query += " AND ReleaseYear >= ?"
        params.append(release_year_from)

    if release_year_to is not None:
        base_query += " AND ReleaseYear <= ?"
        params.append(release_year_to)

    # Total count
    count_query = "SELECT COUNT(*) " + base_query
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]

    # Sorting
    if sort_by is not None:
        column = MediaSortField(sort_by).value
        base_query += f" ORDER BY {column} {order.upper()}"

    # Pagination
    base_query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    # Final query
    final_query = """
        SELECT
            MediaID,
            Title,
            MediaType,
            ReleaseYear,
            Publisher,
            Quantity,
            Price
    """ + base_query

    # Execution
    cursor.execute(final_query, params)
    rows = cursor.fetchall()
    conn.close()

    return (
        [
            Media(
                id=row[0],
                title=row[1],
                media_type=MediaType(row[2]),
                release_year=row[3],
                publisher=row[4],
                quantity=row[5],
                price=row[6],
            )
            for row in rows
        ],
        total,
    )


def update(media: Media) -> Media:
    """
    Updates multiple rows in tblMedia based on MediaID
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tblMedia
        SET
            Title = ?,
            MediaType = ?,
            ReleaseYear = ?,
            Publisher = ?,
            Quantity = ?,
            Price = ?
        WHERE MediaID = ?
        """,
        (
            media.title,
            media.media_type.value,
            media.release_year,
            media.publisher,
            media.quantity,
            media.price,
            media.id,
        ),
    )

    conn.commit()
    conn.close()

    return media


def arithmetics(media_id: int, amount_sold: int) -> bool:
    """
    Single `Price`/`Quantity` value update by selected digit based on the delta.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor = conn.execute(
        """
        UPDATE tblMedia
        SET Quantity = Quantity - ?
        WHERE MediaID = ?
            AND Quantity >= ?
        """,
        (amount_sold, media_id, amount_sold)
    )
    conn.commit()
    conn.close()

    return cursor.rowcount == 1
