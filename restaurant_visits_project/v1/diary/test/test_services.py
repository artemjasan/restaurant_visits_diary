import pytest
import requests  # type: ignore
import responses
from django.conf import settings
from rest_framework import status
from unittest import mock
from v1.diary import services
from v1.diary.test.mock_test_data import CRYPTO_COIN_BTC, CRYPTO_COINS


@responses.activate
@pytest.mark.django_db
def test_crypto_coins_load_success():
    responses.get(
        settings.BASE_URL_API,
        json=CRYPTO_COINS,
        status=200,
    )
    response = services.get_data_from_external_api()
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 2
    for coin in response.json()["data"]:
        assert "id" in coin
        assert "rank" in coin
        assert "name" in coin
        assert "supply" in coin


@responses.activate
@pytest.mark.django_db
def test_crypto_one_coin_load_success():
    coin = CRYPTO_COIN_BTC["data"][0]
    responses.get(
        settings.BASE_URL_API + coin["id"],
        json=CRYPTO_COIN_BTC,
        status=200,
    )
    response = services.get_data_from_external_api(coin["id"])
    data = response.json()["data"]

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1

    assert data[0]["id"] == coin["id"]
    assert data[0]["rank"] == coin["rank"]
    assert data[0]["symbol"] == coin["symbol"]
    assert data[0]["name"] == coin["name"]
    assert data[0]["supply"] == coin["supply"]


@responses.activate
@pytest.mark.django_db
def test_crypto_coins_load_raise_error():
    with mock.patch("v1.diary.services.get_data_from_external_api", side_effect=requests.exceptions.ConnectionError):
        with pytest.raises(requests.exceptions.ConnectionError):
            services.get_data_from_external_api()
