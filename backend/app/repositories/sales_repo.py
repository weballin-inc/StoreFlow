"""tblSales CRUD"""

from app.core.database import get_connection
from app.domain.models import Sale


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