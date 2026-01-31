from typing import List, Optional

from app.core.database import get_connection
from app.domain.models import MediaCopy
from app.domain.enums import CopyStatus
from backend.app.repositories.additional_queries import CopiesSortField


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


def list_filtered(
    copy_id: Optional[int] = None,
    media_id: Optional[int] = None,
    price: Optional[float] = None,
    status: Optional[CopyStatus] = None,
    sort_by: Optional[CopiesSortField] = None,
    order: str = "asc",
    limit: int = 20,
    offset: int = 0,
) -> List[MediaCopy]:

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT CopyID, MediaID, Price, Status
        FROM tblMediaCopies
        WHERE 1 = 1
        """
    
    params = []

    if copy_id is not None:
        query += " AND CopyID = ?"
        params.append(copy_id)

    if media_id is not None:
        query += " AND MediaID = ?"
        params.append(media_id)

    if price is not None:
        query += " AND Price >= ?"
        params.append(price)

    if status is not None:
        query += " AND Status <= ?"
        params.append(status)
 
    if sort_by is not None:
        try:
            column = CopiesSortField(sort_by).value
            query += f" ORDER BY {column} {order.upper()}"
        except ValueError:
            pass

    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    total = len(rows)

    conn.close()

    return [
        MediaCopy(
            id=row[0],
            media_id=row[1],
            price=row[2],
            status=CopyStatus(row[3]),
        )
        for row in rows
    ], total


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


def update_status_with_conn(conn, copy_id: int, status: CopyStatus) -> None:
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tblMediaCopies
        SET Status = ?
        WHERE CopyID = ?
        """,
        (status.value, copy_id),
    )