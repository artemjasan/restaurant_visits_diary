from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from v1.diary.models import Restaurant, Visit
from v1.diary.serializers import restaurant_serializers, visit_serializers


class VisitsViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = visit_serializers.VisitSerializer


class RestaurantsViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.visited_objects.all()
    serializer_class = restaurant_serializers.RestaurantListSerializer

    action_serializer_class_mapping = {
        "create": restaurant_serializers.RestaurantListSerializer,
        "retrieve": restaurant_serializers.RestaurantDetailSerializer,
        "update": restaurant_serializers.RestaurantDetailSerializer,
        "partial_update": restaurant_serializers.RestaurantDetailSerializer,
        "destroy": restaurant_serializers.RestaurantDetailSerializer,
        "add_visit": visit_serializers.BaseVisitSerializer
    }

    def get_serializer_class(self) -> serializers.ModelSerializer:
        return self.action_serializer_class_mapping.get(self.action, super().get_serializer_class())

    @action(detail=True, methods=["post"])
    def add_visit(self, request: Request, *args, **kwargs) -> Response:
        restaurant = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        visit = Visit.objects.create(**serializer.validated_data, creator=request.user, restaurant=restaurant)
        restaurant.visits.add(visit)
        return Response(
            f"A new visit to {restaurant.name} restaurant was successfully added.", status=status.HTTP_200_OK
        )
