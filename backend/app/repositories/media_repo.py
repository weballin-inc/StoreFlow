"""tblMedia CRUD"""

from typing import List, Optional

from app.core.database import get_connection
from app.domain.enums import MediaType
from app.domain.models import Media
from app.repositories.enums_repo import MediaSortField


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

    conn = get_connection()
    cursor = conn.cursor()

    base_query = """
        FROM tblMedia
        WHERE 1 = 1
    """

    params: list = []

    # ---------- exact filters ----------
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

    # ---------- range filters ----------
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

    # ---------- total count ----------
    count_query = "SELECT COUNT(*) " + base_query
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]

    # ---------- sorting ----------
    if sort_by is not None:
        column = MediaSortField(sort_by).value
        base_query += f" ORDER BY {column} {order.upper()}"

    # ---------- pagination ----------
    base_query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    # ---------- final query ----------
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


def update(
    media_id: int,
    title: Optional[str],
    release_year: Optional[int],
    publisher: Optional[str],
    price: Optional[float]
) -> None:
    
    conn = get_connection()
    cursor = conn.cursor()

    fields = []
    params = []

    if title is not None:
        fields.append("Title = ?")
        params.append(title)

    if release_year is not None:
        fields.append("ReleaseYear = ?")
        params.append(release_year)

    if publisher is not None:
        fields.append("Publisher = ?")
        params.append(publisher)

    if price is not None:
        fields.append("Price = ?")
        params.append(price)

    if not fields:
        return  # nothing to update

    query = f"""
        UPDATE tblMedia
        SET {",".join(fields)}
        WHERE MediaID = ?
    """

    cursor.execute(query, params + [media_id])
    conn.commit()
    conn.close()


