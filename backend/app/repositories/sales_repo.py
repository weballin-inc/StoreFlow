"""tblSales CRUD"""

from datetime import datetime

from app.core.database import get_connection
from app.domain.models import Sale
from backend.app.api.routes.sales import SaleResponseSchema


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
