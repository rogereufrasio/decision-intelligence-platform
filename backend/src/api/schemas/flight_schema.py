from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.domain.entities.decision import SortCriterion
from src.domain.entities.flight import FlightOffer


class FlightSearchRequest(BaseModel):
    origin: str = Field(..., min_length=3, max_length=3)
    destination: str = Field(..., min_length=3, max_length=3)
    departure_date: date
    return_date: Optional[date] = None
    passengers: int = Field(default=1, ge=1)
    sort_by: SortCriterion = SortCriterion.BEST_VALUE

    @field_validator("origin", "destination")
    @classmethod
    def validate_iata_code(cls, value: str) -> str:
        if not value.isalpha() or len(value) != 3:
            raise ValueError("IATA code must be a 3-letter alphabetic code")
        return value.upper()


class FlightSearchResponse(BaseModel):
    total_results: int
    applied_criterion: str
    offers: list[FlightOffer] = []
