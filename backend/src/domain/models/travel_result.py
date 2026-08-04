from pydantic import BaseModel, Field
from typing import List

from src.domain.models.offer import Offer


class TravelResult(BaseModel):
    provider: str
    status: str
    message: str
    offers: List[Offer] = Field(default_factory=list)
    metadata: dict | None = None
    warnings: list[str] = Field(default_factory=list)
    execution_time_ms: int | None = None
