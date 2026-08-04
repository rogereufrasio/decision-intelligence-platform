from decimal import Decimal

from pydantic import BaseModel


class Offer(BaseModel):
    provider: str
    product_type: str
    price: Decimal
    currency: str
    metadata: dict | None = None
    attributes: dict | None = None
