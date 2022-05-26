import requests  # type: ignore
from rest_framework.response import Response


def get_data_from_external_api(name: str = None) -> Response:
    """Reqeust external API and get data"""
    if name is None:
        name = ""

    response = requests.request("GET", "http://api.coincap.io/v2/assets/" + name, headers={}, data={})
    response.raise_for_status()
    return response
