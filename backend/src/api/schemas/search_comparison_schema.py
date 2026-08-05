from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SearchComparisonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    base_search_id: str
    target_search_id: str
    currency: str
    base_lowest_price: Decimal
    target_lowest_price: Decimal
    absolute_price_difference: Decimal
    percentage_price_difference: Decimal | None
    base_best_provider: str
    target_best_provider: str
    base_offer_count: int
    target_offer_count: int
    added_providers: list[str] = Field(default_factory=list)
    removed_providers: list[str] = Field(default_factory=list)
