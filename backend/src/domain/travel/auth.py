from datetime import UTC, datetime

from pydantic import BaseModel, Field


class AccessToken(BaseModel):
    access_token: str
    expires_in: int | None = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    def is_expired(
        self,
        safety_margin_seconds: int = 60,
    ) -> bool:

        if not self.expires_in:
            return False

        elapsed = (
            datetime.now(UTC) - self.created_at
        ).total_seconds()

        return elapsed >= (
            self.expires_in - safety_margin_seconds
        )