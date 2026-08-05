from dataclasses import dataclass
from decimal import Decimal

from src.application.ports import SearchRepository
from src.domain.models import Offer, SearchSnapshot


class NoComparableCurrencyError(ValueError):
    pass


@dataclass(frozen=True)
class SearchComparisonResult:
    base_search_id: str
    target_search_id: str
    currency: str
    base_lowest_price: Decimal
    target_lowest_price: Decimal
    absolute_price_difference: Decimal
    percentage_price_difference: Decimal | None
    base_best_provider: str
    target_best_provider: str
    base_offer_count: int
    target_offer_count: int
    added_providers: tuple[str, ...]
    removed_providers: tuple[str, ...]


class CompareSearchSnapshotsUseCase:
    def __init__(self, repository: SearchRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        base_search_id: str,
        target_search_id: str,
    ) -> SearchComparisonResult | None:
        base_snapshot = await self.repository.get(base_search_id)
        target_snapshot = await self.repository.get(target_search_id)

        if base_snapshot is None or target_snapshot is None:
            return None

        currency = self._select_comparable_currency(
            base_snapshot,
            target_snapshot,
        )
        base_offers = self._offers_for_currency(base_snapshot, currency)
        target_offers = self._offers_for_currency(
            target_snapshot,
            currency,
        )
        base_best_offer = self._best_offer(base_offers)
        target_best_offer = self._best_offer(target_offers)
        price_change = target_best_offer.price - base_best_offer.price
        percentage_change = (
            price_change / base_best_offer.price * Decimal("100")
            if base_best_offer.price != 0
            else None
        )
        base_providers = {offer.provider for offer in base_offers}
        target_providers = {offer.provider for offer in target_offers}

        return SearchComparisonResult(
            base_search_id=base_search_id,
            target_search_id=target_search_id,
            currency=currency,
            base_lowest_price=base_best_offer.price,
            target_lowest_price=target_best_offer.price,
            absolute_price_difference=abs(price_change),
            percentage_price_difference=percentage_change,
            base_best_provider=base_best_offer.provider,
            target_best_provider=target_best_offer.provider,
            base_offer_count=len(base_offers),
            target_offer_count=len(target_offers),
            added_providers=tuple(sorted(target_providers - base_providers)),
            removed_providers=tuple(sorted(base_providers - target_providers)),
        )

    @staticmethod
    def _select_comparable_currency(
        base_snapshot: SearchSnapshot,
        target_snapshot: SearchSnapshot,
    ) -> str:
        base_currencies = {offer.currency for offer in base_snapshot.offers}
        target_currencies = {
            offer.currency for offer in target_snapshot.offers
        }
        comparable_currencies = sorted(
            base_currencies & target_currencies
        )

        if not comparable_currencies:
            raise NoComparableCurrencyError(
                "The snapshots do not contain offers in a common currency."
            )

        return comparable_currencies[0]

    @staticmethod
    def _offers_for_currency(
        snapshot: SearchSnapshot,
        currency: str,
    ) -> list[Offer]:
        return [
            offer
            for offer in snapshot.offers
            if offer.currency == currency
        ]

    @staticmethod
    def _best_offer(offers: list[Offer]) -> Offer:
        return min(
            offers,
            key=lambda offer: (offer.price, offer.provider),
        )
