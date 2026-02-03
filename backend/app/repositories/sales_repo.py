"""tblSales CRUD"""

from datetime import datetime

from app.core.database import get_connection
from app.domain.models import Sale
from backend.app.api.schemas.sales import SaleResponseSchema
from backend.app.api.schemas.sales_query import SalesSortField


def insert_sale(media_id: int, price: float) -> SaleResponseSchema:
    conn = get_connection()
    cursor = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor = conn.execute(
        """
        INSERT INTO tblSales (MediaID, Price, Date)
        VALUES (?, ?, ?)
        """,
        (
            media_id,
            price,
            current_date
        ),
    )

    conn.commit()
    conn.close()

    return Sale(
        id=cursor.lastrowid,
        media_id=media_id,
        price=price,
        date=current_date
    )


def list_filtered(
    sale_id: int | None = None,
    media_id: int | None = None,

    price: int | None = None,
    price_from: int | None = None,
    price_to: int | None = None,

    date: int | None = None,
    date_from: int | None = None,
    date_to: int | None = None,

    sort_by: str | None = None,
    order: str = "asc",
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[Sale], int]:

    conn = get_connection()
    cursor = conn.cursor()

    base_query = """
        FROM tblSales
        WHERE 1 = 1
    """

    params: list = []

    # ---------- exact filters ----------
    if sale_id is not None:
        base_query += " AND SaleID = ?"
        params.append(sale_id)

    if media_id is not None:
        base_query += " AND MediaID = ?"
        params.append(media_id)

    if price is not None:
        base_query += " AND Price = ?"
        params.append(price)

    if date is not None:
        base_query += " AND ReleaseYear = ?"
        params.append(date)

    # ---------- range filters ----------

    if price_from is not None:
        base_query += " AND Price >= ?"
        params.append(price_from)

    if price_to is not None:
        base_query += " AND Price <= ?"
        params.append(price_to)

    if date_from is not None:
        base_query += " AND ReleaseYear >= ?"
        params.append(date_from)

    if date_to is not None:
        base_query += " AND ReleaseYear <= ?"
        params.append(date_to)

    # ---------- total count ----------
    count_query = "SELECT COUNT(*) " + base_query
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]

    # ---------- sorting ----------
    if sort_by is not None:
        column = SalesSortField(sort_by).value
        base_query += f" ORDER BY {column} {order.upper()}"

    # ---------- pagination ----------
    base_query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    # ---------- final query ----------
    final_query = """
        SELECT
            SaleID,
            MediaID,
            Price,
            Date
    """ + base_query

    cursor.execute(final_query, params)
    rows = cursor.fetchall()
    conn.close()

    return (
        [
            Sale(
                id=row[0],
                media_id=row[1],
                price=row[2],
                date=row[3]
            )
            for row in rows
        ],
        total,
    )