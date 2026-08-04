from pydantic import BaseModel


class FlightSegment(BaseModel):
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    duration_minutes: int
    carrier: str | None = None
    flight_number: str | None = None


class FlightSlice(BaseModel):
    origin: str
    destination: str
    departure_date: str
    arrival_date: str
    duration_minutes: int
    segments: list[FlightSegment] = []


class FlightOffer(BaseModel):
    id: str | None = None
    provider: str
    total_amount: str
    currency: str
    total_duration_minutes: int
    slices: list[FlightSlice] = []
