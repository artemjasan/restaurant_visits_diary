from drf_spectacular import utils as spec_utils
from rest_framework import response, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import CharField, URLField
from v1.diary import services


class CryptoViews(views.APIView):
    permission_classes = [IsAuthenticated]

    @spec_utils.extend_schema(
        description="Provides, list of crypto coins.",
        responses={
            status.HTTP_200_OK: spec_utils.OpenApiResponse(
                description="Successfully downloaded crypto coin(s) information.",
                response=spec_utils.inline_serializer(
                    name="LinkExistsOutput",
                    fields={
                        "id": CharField(),
                        "rank": CharField(),
                        "symbol": CharField(),
                        "supply": CharField(),
                        "maxSupply": CharField(),
                        "marketCapUSD": CharField(),
                        "volumeUsd24Hr": CharField(),
                        "priceUsd": CharField(),
                        "changePercent24Hr": CharField(),
                        "vwap24Hr": CharField(),
                        "explorer": URLField(),
                    },
                ),
            ),
        },
    )
    def get(self, request, format=None):
        coin_name = self.request.query_params.get("name")
        service_response = services.get_data_from_external_api(name=coin_name)
        return response.Response(data=service_response.json(), status=service_response.status_code)
