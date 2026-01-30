"""tblSales CRUD"""

from typing import List, Dict, Optional

from app.core.database import get_connection
from app.domain.models import Sale
from app.repositories.additional_queries import SalesSortField


def list_filtered(
    media_type: Optional[str] = None,
    publisher: Optional[str] = None,
    release_year_from: Optional[int] = None,
    release_year_to: Optional[int] = None,
    copy_id: Optional[int] = None,
    media_id: Optional[int] = None,
    sort_by: Optional[str] = None,
    order: str = "asc",
    limit: int = 20,
    offset: int = 0,
) -> List[Dict]:

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            s.SaleID,
            s.Price,
            c.CopyID,
            m.MediaID,
            m.Title,
            m.MediaType,
            m.ReleaseYear,
            m.Publisher

        FROM tblSales s
        JOIN tblMediaCopies c ON s.CopyID = c.CopyID
        JOIN tblMediaTitles m ON c.MediaID = m.MediaID

        WHERE 1 = 1
    """

    params = []

    # -------- FILTRY --------

    if copy_id is not None:
        query += " AND c.CopyID = ?"
        params.append(copy_id)

    if media_id is not None:
        query += " AND m.MediaID = ?"
        params.append(media_id)

    if media_type is not None:
        query += " AND m.MediaType = ?"
        params.append(media_type)

    if publisher is not None:
        query += " AND m.Publisher = ?"
        params.append(publisher)

    if release_year_from is not None:
        query += " AND m.ReleaseYear >= ?"
        params.append(release_year_from)

    if release_year_to is not None:
        query += " AND m.ReleaseYear <= ?"
        params.append(release_year_to)

    # -------- SORTOWANIE --------

    if sort_by is not None:
        try:
            column = SalesSortField(sort_by).value
            query += f" ORDER BY {column} {order.upper()}"
        except ValueError:
            pass
    else:
        query += " ORDER BY s.SaleID DESC"

    # -------- PAGINACJA --------

    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    print(query)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append(
            {
                "sale_id": row[0],
                "sale_price": row[1],
                "copy_id": row[2],
                "media": {
                    "media_id": row[3],
                    "title": row[4],
                    "media_type": row[5],
                    "release_year": row[6],
                    "publisher": row[7],
                },
            }
        )

    return results


def get_by_id(sale_id: int) -> Optional[Sale]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT SaleID, CopyID, Price
        FROM tblSales
        WHERE SaleID = ?
        """,
        (sale_id,),
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return Sale(
        id=row[0],
        copy_id=row[1],
        price=row[2],
    )


def create(sale: Sale) -> Sale:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tblSales (CopyID, Price)
        VALUES (?, ?)
        """,
        (sale.copy_id, sale.price),
    )

    conn.commit()

    return Sale(
        id=cursor.lastrowid,
        copy_id=sale.copy_id,
        price=sale.price,
    )


def create_with_conn(conn, sale: Sale) -> Sale:
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tblSales (CopyID, Price)
        VALUES (?, ?)
        """,
        (sale.copy_id, sale.price),
    )

    return Sale(
        id=cursor.lastrowid,
        copy_id=sale.copy_id,
        price=sale.price
    )

