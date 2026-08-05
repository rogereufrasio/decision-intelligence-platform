from pydantic import BaseModel, ConfigDict


class AIExplanation(BaseModel):
    model_config = ConfigDict(frozen=True)

    summary: str
    reasons: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
