from typing import Final

BASE_RESTAURANTS_URL: Final = "http://127.0.0.1:8000/api/v1/restaurants/"
BASE_VISIT_URL: Final = "http://127.0.0.1:8000/api/v1/visits/"
BASE_CRYPTO_URL: Final = "http://127.0.0.1:8000/api/v1/crypto/"

RESTAURANT_DATA_BASE: Final = {"name": "Test restaurant", "city": "Prague", "cuisine": "Czech"}

# For testing purposes generate simplified response data with limited numbers of fields.
CRYPTO_COINS: Final = {
    "data": [
        {"id": "bitcoin", "rank": "1", "symbol": "BTC", "name": "Bitcoin", "supply": "19050012.0000000000000000"},
        {"id": "ethereum", "rank": "2", "symbol": "ETH", "name": "Ethereum", "supply": "120931330.1865000000000000"},
    ]
}

CRYPTO_COIN_BTC: Final = {
    "data": [
        {"id": "bitcoin", "rank": "1", "symbol": "BTC", "name": "Bitcoin", "supply": "19050012.0000000000000000"},
    ]
}
