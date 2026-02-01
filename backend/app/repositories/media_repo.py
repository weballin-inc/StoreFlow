"""tblMedia CRUD"""

from typing import List, Optional

from app.core.database import get_connection
from app.domain.enums import MediaType
from app.domain.models import Media
from app.repositories.enums_repo import MediaSortField


def list_filtered(
    media_type: Optional[MediaType] = None,
    publisher: Optional[str] = None,
    release_year: Optional[int] = None,
    release_year_from: Optional[int] = None,
    release_year_to: Optional[int] = None,
    sort_by: Optional[str] = None,
    order: str = "asc",
    limit: int = 20,
    offset: int = 0,
) -> List[Media]:

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT MediaID, Title, MediaType, ReleaseYear, Publisher
        FROM tblMedia
        WHERE 1 = 1
    """
    params = []

    if media_type is not None:
        query += " AND MediaType = ?"
        params.append(media_type.value)

    if publisher is not None:
        query += " AND Publisher = ?"
        params.append(publisher)

    if release_year_from is not None:
        query += " AND ReleaseYear >= ?"
        params.append(release_year_from)

    if release_year_to is not None:
        query += " AND ReleaseYear <= ?"
        params.append(release_year_to)

    if release_year is not None:
        query += " AND ReleaseYear = ?"
        params.append(release_year)

    if sort_by is not None:
        try:
            column = MediaSortField(sort_by).value
            query += f" ORDER BY {column} {order.upper()}"
        except ValueError:
            pass

    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    total = len(rows)

    return [
        Media(
            id=row[0],
            title=row[1],
            media_type=MediaType(row[2]),
            release_year=row[3],
            publisher=row[4],
        )
        for row in rows
    ], total


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
            ReleaseYear, Publisher, Amount, Price
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
        amount=row[5],
        price=row[6]
    )


def get_by_id(media_id: int) -> Optional[Media]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MediaID, Title, MediaType, ReleaseYear, Publisher, Amount, Price
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
        amount=row[5],
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
        INSERT INTO tblMedia (Title, MediaType, ReleaseYear, Publisher, Amount, Price)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            media.title,
            media.media_type.value,
            media.release_year,
            media.publisher,
            media.amount,
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
        amount=media.amount,
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


