from typing import List, Optional

from app.core.database import get_connection
from app.domain.models import MediaCopy
from app.domain.enums import CopyStatus


def create(copy: MediaCopy) -> MediaCopy:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tblMediaCopies (MediaID, Price, Status)
        VALUES (?, ?, ?)
        """,
        (
            copy.media_id,
            copy.price,
            copy.status,
        ),
    )

    conn.commit()

    return MediaCopy(
        id=cursor.lastrowid,
        media_id=copy.media_id,
        price=copy.price,
        status=copy.status,
    )


def get_by_id(copy_id: int) -> Optional[MediaCopy]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT CopyID, MediaID, Price, Status
        FROM tblMediaCopies
        WHERE CopyID = ?
        """,
        (copy_id,),
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return MediaCopy(
        id=row[0],
        media_id=row[1],
        price=row[2],
        status=CopyStatus(row[3]),
    )


def update_status(copy_id: int, status: CopyStatus) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tblMediaCopies
        SET Status = ?
        WHERE CopyID = ?
        """,
        (status.value, copy_id),
    )

    conn.commit()