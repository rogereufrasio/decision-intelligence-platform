from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.domain.entities.decision import SortCriterion
from src.domain.models.offer import Offer
from src.domain.models.search_criteria import SearchCriteria


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SearchSnapshot(BaseModel):
    model_config = ConfigDict(frozen=True)

    search_id: str
    criteria: SearchCriteria
    created_at: datetime = Field(default_factory=utc_now)
    provider: str
    status: str
    offers: list[Offer] = Field(default_factory=list)
    sort_criterion: SortCriterion | None = None
    schema_version: str = "1.0"
    correlation_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)

    @field_validator("created_at")
    @classmethod
    def ensure_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")
        return value.astimezone(timezone.utc)
