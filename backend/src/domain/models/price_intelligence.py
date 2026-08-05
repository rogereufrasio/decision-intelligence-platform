from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class PriceTrend(str, Enum):
    DECREASED = "decreased"
    INCREASED = "increased"
    STABLE = "stable"
    INSUFFICIENT_DATA = "insufficient_data"


class PriceIntelligence(BaseModel):
    model_config = ConfigDict(frozen=True)

    current_price: Decimal | None = None
    previous_price: Decimal | None = None
    historical_min: Decimal | None = None
    historical_max: Decimal | None = None
    historical_average: Decimal | None = None
    absolute_change: Decimal | None = None
    percentage_change: Decimal | None = None
    trend: PriceTrend
    snapshot_count: int = Field(ge=0)
    currency: str | None = None
