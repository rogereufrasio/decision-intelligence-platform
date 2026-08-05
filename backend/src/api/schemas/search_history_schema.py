from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.domain.entities.decision import SortCriterion


class SearchCriteriaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    origin: str
    destination: str
    departure_date: date
    return_date: date | None = None
    adults: int


class SearchOfferResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    provider: str
    product_type: str
    price: Decimal
    currency: str
    metadata: dict[str, Any] | None = None
    attributes: dict[str, Any] | None = None


class SearchSnapshotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    search_id: str
    criteria: SearchCriteriaResponse
    created_at: datetime
    provider: str
    status: str
    offers: list[SearchOfferResponse] = Field(default_factory=list)
    sort_criterion: SortCriterion | None = None
    schema_version: str
    correlation_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)


class SearchHistoryResponse(BaseModel):
    items: list[SearchSnapshotResponse] = Field(default_factory=list)
    total: int
