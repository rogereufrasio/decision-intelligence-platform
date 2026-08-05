from decimal import Decimal

from src.domain.models import (
    PriceIntelligence,
    PriceTrend,
    SearchSnapshot,
)


class PriceIntelligenceEngine:
    STABLE_THRESHOLD_PERCENT = Decimal("1")

    def analyze(
        self,
        snapshots: list[SearchSnapshot],
    ) -> PriceIntelligence:
        if not snapshots:
            return self._insufficient_result()

        base_snapshot = snapshots[0]
        currency = self._reference_currency(base_snapshot)
        if currency is None:
            return self._insufficient_result()

        comparable_snapshots = [
            snapshot
            for snapshot in snapshots
            if snapshot.criteria == base_snapshot.criteria
        ]
        price_points = [
            (snapshot, price)
            for snapshot in comparable_snapshots
            if (
                price := self._lowest_price(snapshot, currency)
            )
            is not None
        ]
        price_points.sort(
            key=lambda item: (
                item[0].created_at,
                item[0].search_id,
            ),
            reverse=True,
        )

        if not price_points:
            return self._insufficient_result(currency=currency)

        prices = [price for _, price in price_points]
        current_price = prices[0]
        historical_average = sum(prices, Decimal("0")) / Decimal(
            len(prices)
        )

        if len(prices) == 1:
            return PriceIntelligence(
                current_price=current_price,
                historical_min=current_price,
                historical_max=current_price,
                historical_average=historical_average,
                trend=PriceTrend.INSUFFICIENT_DATA,
                snapshot_count=1,
                currency=currency,
            )

        previous_price = prices[1]
        absolute_change = current_price - previous_price
        percentage_change = (
            absolute_change / previous_price * Decimal("100")
            if previous_price != 0
            else None
        )

        return PriceIntelligence(
            current_price=current_price,
            previous_price=previous_price,
            historical_min=min(prices),
            historical_max=max(prices),
            historical_average=historical_average,
            absolute_change=absolute_change,
            percentage_change=percentage_change,
            trend=self._classify(absolute_change, percentage_change),
            snapshot_count=len(prices),
            currency=currency,
        )

    @staticmethod
    def _reference_currency(snapshot: SearchSnapshot) -> str | None:
        if not snapshot.offers:
            return None
        best_offer = min(
            snapshot.offers,
            key=lambda offer: (
                offer.price,
                offer.currency,
                offer.provider,
            ),
        )
        return best_offer.currency

    @staticmethod
    def _lowest_price(
        snapshot: SearchSnapshot,
        currency: str,
    ) -> Decimal | None:
        prices = [
            offer.price
            for offer in snapshot.offers
            if offer.currency == currency
        ]
        return min(prices) if prices else None

    def _classify(
        self,
        absolute_change: Decimal,
        percentage_change: Decimal | None,
    ) -> PriceTrend:
        if percentage_change is not None:
            if abs(percentage_change) < self.STABLE_THRESHOLD_PERCENT:
                return PriceTrend.STABLE
        elif absolute_change == 0:
            return PriceTrend.STABLE

        if absolute_change < 0:
            return PriceTrend.DECREASED
        return PriceTrend.INCREASED

    @staticmethod
    def _insufficient_result(
        currency: str | None = None,
    ) -> PriceIntelligence:
        return PriceIntelligence(
            trend=PriceTrend.INSUFFICIENT_DATA,
            snapshot_count=0,
            currency=currency,
        )
