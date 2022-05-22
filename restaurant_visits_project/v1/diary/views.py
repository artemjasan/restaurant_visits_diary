from rest_framework import serializers, viewsets

from .models import Restaurant, Visit
from .serializers import RestaurantListSerializer, RestaurantDetailSerializer, VisitSerializer


class VisitsViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer


class RestaurantsViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.visited_objects.all()
    serializer_class = RestaurantListSerializer

    action_serializer_class_mapping = {
        "create": RestaurantListSerializer,
        "retrieve": RestaurantDetailSerializer,
        "update": RestaurantDetailSerializer,
        "partial_update": RestaurantDetailSerializer,
        "destroy": RestaurantDetailSerializer,
    }

    def get_serializer_class(self) -> serializers.ModelSerializer:
        return self.action_serializer_class_mapping.get(self.action, super().get_serializer_class())

