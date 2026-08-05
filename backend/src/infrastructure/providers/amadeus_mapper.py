from src.domain.models import Offer as TravelOffer


class AmadeusMapper:
    @staticmethod
    def normalize_offers(data: dict) -> list[TravelOffer]:
        offers = []
        for item in data.get("data", []):
            price = item.get("price", {})
            offers.append(
                TravelOffer(
                    provider="amadeus",
                    product_type="flight",
                    price=price.get("grandTotal", "0.00"),
                    currency=price.get("currency", "BRL"),
                )
            )
        return offers
