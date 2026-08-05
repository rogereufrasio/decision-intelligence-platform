from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from src.domain.models import PriceTrend


class PriceIntelligenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    current_price: Decimal | None = None
    previous_price: Decimal | None = None
    historical_min: Decimal | None = None
    historical_max: Decimal | None = None
    historical_average: Decimal | None = None
    absolute_change: Decimal | None = None
    percentage_change: Decimal | None = None
    trend: PriceTrend
    snapshot_count: int
    currency: str | None = None
