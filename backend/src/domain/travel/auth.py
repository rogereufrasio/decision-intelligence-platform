from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    expires_in: int | None = None