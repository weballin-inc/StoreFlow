"""tblMediaTitles CRUD"""

from typing import List, Optional

from app.core.database import get_connection
from app.domain.models import MediaTitle
from app.domain.enums import MediaType
from app.repositories.additional_queries import MediaSortField


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
) -> List[MediaTitle]:

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT MediaID, Title, MediaType, ReleaseYear, Publisher
        FROM tblMediaTitles
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
        MediaTitle(
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
) -> Optional[MediaTitle]:
    """
    Returns Title if found, otherwise None.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MediaID, Title, MediaType, ReleaseYear, Publisher
        FROM tblMediaTitles
        WHERE Title = ? AND MediaType = ?
        """,
        (title, media_type.value),
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return MediaTitle(
        id=row[0],
        title=row[1],
        media_type=MediaType(row[2]),
        release_year=row[3],
        publisher=row[4],
    )


def get_by_id(media_id: int) -> Optional[MediaTitle]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MediaID, Title, MediaType, ReleaseYear, Publisher
        FROM tblMediaTitles
        WHERE MediaID = ?
        """,
        (media_id,),
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return MediaTitle(
        id=row[0],
        title=row[1],
        media_type=MediaType(row[2]),
        release_year=row[3],
        publisher=row[4],
    )


# Used to insert
def create(media: MediaTitle) -> MediaTitle:
    """
    Inserts a new MediaTitle into the database and returns it with ID.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tblMediaTitles (Title, MediaType, ReleaseYear, Publisher)
        VALUES (?, ?, ?, ?)
        """,
        (
            media.title,
            media.media_type.value,
            media.release_year,
            media.publisher
        ),
    )

    conn.commit()

    return MediaTitle(
        id=cursor.lastrowid,
        title=media.title,
        media_type=media.media_type,
        release_year=media.release_year,
        publisher=media.publisher,
    )