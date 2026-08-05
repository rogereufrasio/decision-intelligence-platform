from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PreferenceProfileName(str, Enum):
    CHEAPEST = "cheapest"
    FASTEST = "fastest"
    BALANCED = "balanced"
    PREMIUM = "premium"


class PreferenceProfile(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: PreferenceProfileName
    price_weight: Decimal = Field(ge=0, le=1)
    duration_weight: Decimal = Field(ge=0, le=1)
    provider_weight: Decimal = Field(ge=0, le=1)
    preferred_providers: tuple[str, ...] = ()

    @model_validator(mode="after")
    def validate_weight_total(self) -> "PreferenceProfile":
        total = (
            self.price_weight
            + self.duration_weight
            + self.provider_weight
        )
        if total != Decimal("1"):
            raise ValueError("preference profile weights must sum to 1")
        return self

    @classmethod
    def cheapest(
        cls,
        preferred_providers: tuple[str, ...] = (),
    ) -> "PreferenceProfile":
        return cls(
            name=PreferenceProfileName.CHEAPEST,
            price_weight=Decimal("0.70"),
            duration_weight=Decimal("0.20"),
            provider_weight=Decimal("0.10"),
            preferred_providers=preferred_providers,
        )

    @classmethod
    def fastest(
        cls,
        preferred_providers: tuple[str, ...] = (),
    ) -> "PreferenceProfile":
        return cls(
            name=PreferenceProfileName.FASTEST,
            price_weight=Decimal("0.20"),
            duration_weight=Decimal("0.70"),
            provider_weight=Decimal("0.10"),
            preferred_providers=preferred_providers,
        )

    @classmethod
    def balanced(
        cls,
        preferred_providers: tuple[str, ...] = (),
    ) -> "PreferenceProfile":
        return cls(
            name=PreferenceProfileName.BALANCED,
            price_weight=Decimal("0.45"),
            duration_weight=Decimal("0.45"),
            provider_weight=Decimal("0.10"),
            preferred_providers=preferred_providers,
        )

    @classmethod
    def premium(
        cls,
        preferred_providers: tuple[str, ...] = (),
    ) -> "PreferenceProfile":
        return cls(
            name=PreferenceProfileName.PREMIUM,
            price_weight=Decimal("0.20"),
            duration_weight=Decimal("0.20"),
            provider_weight=Decimal("0.60"),
            preferred_providers=preferred_providers,
        )
