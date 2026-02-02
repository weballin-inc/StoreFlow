"""Business logic for tblSales"""

from app.core.database import get_connection
from app.domain.models import Sale
from app.repositories import sales_repo

############################################
#   tblSales
############################################
# def sell_copy(copy_id: int) -> Sale:
#     conn = get_connection()

#     try:
#         conn.execute("BEGIN")

#         copy = copies_repo.get_by_id(copy_id)
#         if copy is None:
#             raise CopyNotFoundError(f"Copy with ID {copy_id} not found")

#         if copy.status == CopyStatus.SOLD:
#             raise CopyAlreadySoldError(f"Copy with ID {copy_id} already sold")

#         sale = Sale(
#             id=copy.id,
#             copy_id=copy_id,
#             price=copy.price,
#         )

#         created_sale = sales_repo.create_with_conn(conn, sale)

#         copies_repo.update_status_with_conn(conn, sale.id, CopyStatus.SOLD)

#         conn.commit()
#         return created_sale

#     except:
#         conn.rollback()
#         raise

#     finally:
#         conn.close()
