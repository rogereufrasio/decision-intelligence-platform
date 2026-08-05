from src.core.config import get_settings
from src.domain.travel.models import TravelOffer, TravelResult
from src.domain.travel.provider import TravelProvider
from src.infrastructure.http.client import HttpClient
from src.infrastructure.http.exceptions import HttpClientException
from src.infrastructure.providers.base_provider import BaseProvider
from src.shared.models import TravelSearchRequest


class DuffelProvider(
    BaseProvider,
    TravelProvider,
):

    def __init__(
        self,
        client: HttpClient,
        base_url: str | None = None,
    ):
        settings = get_settings()

        super().__init__(
            client=client,
            base_url=(
                base_url
                or settings.duffel_base_url
            ),
        )
        self.api_key = settings.duffel_api_key

    async def search(
        self,
        request: TravelSearchRequest,
    ) -> TravelResult:
        if not self.api_key:
            raise ValueError(
                "Duffel API key is not configured"
            )

        payload = {
            "slices": [
                {
                    "origin": request.origin,
                    "destination": request.destination,
                    "departure_date": request.departure_date,
                }
            ],
            "passengers": [
                {"type": "adult"}
                for _ in range(request.adults)
            ],
        }

        if request.return_date:
            payload["slices"].append(
                {
                    "origin": request.destination,
                    "destination": request.origin,
                    "departure_date": request.return_date,
                }
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = await self.post(
                "/air/offer_requests",
                json=payload,
                headers=headers,
            )
        except HttpClientException as exc:
            return TravelResult(
                provider="duffel",
                status="error",
                message=f"Duffel search failed: {exc}",
                offers=[],
            )

        offers = self._normalize_offers(
            response.json(),
        )

        return TravelResult(
            provider="duffel",
            status="success",
            message="Offers retrieved successfully",
            offers=offers,
        )

    def _normalize_offers(
        self,
        payload: dict,
    ) -> list[TravelOffer]:
        offers: list[TravelOffer] = []
        items = payload.get("data")

        if items is None:
            return offers

        if isinstance(items, dict):
            items = [items]

        for item in items:
            if not isinstance(item, dict):
                continue

            if "offers" in item and isinstance(item["offers"], list):
                for raw_offer in item["offers"]:
                    price = raw_offer.get("total_amount")
                    currency = raw_offer.get("total_currency")
                    if price and currency:
                        offers.append(
                            TravelOffer(
                                provider="duffel",
                                product_type="flight",
                                price=str(price),
                                currency=str(currency),
                            )
                        )
            else:
                price = item.get("total_amount") or item.get("total_price")
                currency = (
                    item.get("currency")
                    or item.get("total_currency")
                )
                if price and currency:
                    offers.append(
                        TravelOffer(
                            provider="duffel",
                            product_type="flight",
                            price=str(price),
                            currency=str(currency),
                        )
                    )

        return offers