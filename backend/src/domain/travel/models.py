from pydantic import BaseModel


class TravelOffer(BaseModel):
    price: str
    currency: str


class TravelResult(BaseModel):
    provider: str
    status: str
    message: str
    offers: list[TravelOffer] = []