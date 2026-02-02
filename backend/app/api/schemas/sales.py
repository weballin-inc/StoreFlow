from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

# ---------- Create ----------

class SaleCreateSchema(BaseModel):
    media_id: int = Field(..., ge=1)

# ---------- Response ----------

class SaleResponseSchema(SaleCreateSchema):
    id: int
    price: float
    date: datetime

# ---------- Paged ----------

class PagedSalesResponseSchema(BaseModel):
    items: List[Dict]
    total: int
    limit: int
    offset: int