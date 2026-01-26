"""tblMediaTitles CRUD"""

from typing import List, Optional

from app.core.database import get_connection
from app.domain.models import MediaTitle
from app.domain.enums import MediaType
from app.repositories.media_queries import MediaSortField


def list_filtered(
    media_type: Optional[MediaType] = None,
    publisher: Optional[str] = None,
    release_year: Optional[int] = None,
    sort_by: Optional[str] = None,
    order: str = "asc",
) -> List[MediaTitle]:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT MediaID, MediaTitle, MediaType, MediaReleaseYear, MediaPublisher
        FROM tblMediaTitles
        WHERE 1 = 1
    """
    params = []

    if media_type is not None:
        query += " AND MediaType = ?"
        params.append(media_type.value)

    if publisher is not None:
        query += " AND MediaPublisher = ?"
        params.append(publisher)

    if release_year is not None:
        query += " AND MediaReleaseYear = ?"
        params.append(release_year)

    if sort_by is not None:
        try:
            column = MediaSortField(sort_by).value
            query += f" ORDER BY {column} {order.upper()}"
        except ValueError:
            pass

    cursor.execute(query, params)
    rows = cursor.fetchall()

    return [
        MediaTitle(
            id=row[0],
            title=row[1],
            media_type=MediaType(row[2]),
            release_year=row[3],
            publisher=row[4],
        )
        for row in rows
    ]


# Used to query if inserting a potential duplicate
def get_by_title_and_type(
    title: str,
    media_type: MediaType
) -> Optional[MediaTitle]:
    """
    Returns MediaTitle if found, otherwise None.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MediaID, MediaTitle, MediaType, MediaReleaseYear, MediaPublisher
        FROM tblMediaTitles
        WHERE MediaTitle = ? AND MediaType = ?
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

# Used to insert
def create(media: MediaTitle) -> MediaTitle:
    """
    Inserts a new MediaTitle into the database and returns it with ID.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tblMediaTitles (MediaTitle, MediaType, MediaReleaseYear, MediaPublisher)
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