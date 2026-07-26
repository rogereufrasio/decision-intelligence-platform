from pydantic import BaseModel


class TravelResult(BaseModel):
    provider: str
    status: str
    message: str