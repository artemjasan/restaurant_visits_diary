from rest_framework import serializers

from v1.diary.models import Restaurant
from v1.diary.serializers import visit_serializers


class RestaurantListSerializer(serializers.ModelSerializer):
    visits = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    creator = serializers.HiddenField(default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()))

    class Meta:
        model = Restaurant
        fields = ("id", "name", "city", "cuisine", "visits", "creator")


class RestaurantDetailSerializer(RestaurantListSerializer):
    visits = visit_serializers.VisitSerializer(many=True, read_only=True)
