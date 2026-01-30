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