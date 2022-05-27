import pytest
from rest_framework.test import APIClient
from unittest import mock

from .conftest import try_all_authentications_with_codes
from .mock_test_data import BASE_CRYPTO_URL


def _generate_mocked_response(status_code: int = 200, data=None) -> mock.Mock:
    if data is None:
        data = dict()
    mocked_response = mock.Mock()
    mocked_response.status_code = status_code
    mocked_response.json.return_value = data

    return mocked_response


@pytest.mark.django_db
@pytest.mark.parametrize(**try_all_authentications_with_codes(401, 200, 200))
def test_get_all_crypto_list_different_auths_status_code(configured_api_client: APIClient, status_code: int):
    with mock.patch("v1.diary.services.get_data_from_external_api", return_value=_generate_mocked_response()):
        response = configured_api_client.get(BASE_CRYPTO_URL)
        assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(**try_all_authentications_with_codes(401, 200, 200))
def test_get_required_crypto_list_different_auths_status_code(configured_api_client: APIClient, status_code: int):
    with mock.patch("v1.diary.services.get_data_from_external_api", return_value=_generate_mocked_response()):
        response = configured_api_client.get(BASE_CRYPTO_URL + "?name=bitcoin")
        assert response.status_code == status_code
