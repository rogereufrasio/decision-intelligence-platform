from pydantic import BaseModel, Field


class TravelSearchRequest(BaseModel):
    origin: str = Field(..., min_length=3)
    destination: str = Field(..., min_length=3)
    departure_date: str
    return_date: str | None = None
    adults: int = Field(default=1, ge=1)


class TravelOfferResponse(BaseModel):
    price: str
    currency: str


class TravelSearchResponse(BaseModel):
    provider: str
    status: str
    message: str
    offers: list[TravelOfferResponse] = []