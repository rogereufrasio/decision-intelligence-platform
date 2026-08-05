from src.infrastructure.providers.amadeus_mapper import (
    AmadeusMapper,
)


def test_normalize_amadeus_response():

    data = {
        "data": [
            {
                "price": {
                    "grandTotal": "450.00",
                    "currency": "BRL",
                }
            }
        ]
    }

    offers = AmadeusMapper.normalize_offers(
        data
    )

    assert len(offers) == 1
    assert str(offers[0].price) == "450.00"
    assert offers[0].currency == "BRL"