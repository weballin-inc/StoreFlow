"""tblMediaTitles CRUD"""

from typing import Optional

from app.core.database import get_connection
from app.domain.models import MediaTitle
from app.domain.enums import MediaType


def get_all() -> list[MediaTitle]:
    """
    Returns all media titles from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MediaID, MediaTitle, MediaType, MediaReleaseYear, MediaPublisher
        FROM tblMediaTitles
        """
    )

    rows = cursor.fetchall()

    result: list[MediaTitle] = []

    for row in rows:
        result.append(
            MediaTitle(
                id=row[0],
                title=row[1],
                media_type=MediaType(row[2]),
                release_year=row[3],
                publisher=row[4],
            )
        )

    return result


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