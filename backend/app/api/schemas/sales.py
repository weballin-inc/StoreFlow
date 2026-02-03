from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

# ---------- Create ----------

class SaleCreateSchema(BaseModel):
    amount_sold: int = Field(gt=0)

# ---------- Response ----------

class SaleResponseSchema(BaseModel):
    id: int
    media_id: int
    price: float
    date: datetime

# ---------- Paged ----------

class PagedSaleResponseSchema(BaseModel):
    items: List[SaleResponseSchema]
    total: int
    limit: int
    offset: int