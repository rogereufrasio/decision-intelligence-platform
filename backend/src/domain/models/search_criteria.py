from datetime import date

from pydantic import BaseModel, Field


class SearchCriteria(BaseModel):
    origin: str = Field(min_length=3)
    destination: str = Field(min_length=3)
    departure_date: date
    return_date: date | None = None
    adults: int = Field(default=1, ge=1)
