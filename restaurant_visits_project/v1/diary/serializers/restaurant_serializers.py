from typing import Any

from rest_framework import serializers

from v1.diary.models import Restaurant
from v1.diary.serializers import visit_serializers


class RestaurantListSerializer(serializers.ModelSerializer):
    visits = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    creator = serializers.HiddenField(default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()))
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj) -> float:
        return obj.average_rating

    def to_representation(self, instance) -> dict[str, Any]:
        representation = super().to_representation(instance)  # type: ignore
        representation["average_rating"] = round(instance.average_rating, 1)
        return representation

    class Meta:
        model = Restaurant
        fields = ("id", "name", "city", "cuisine", "creator", "average_rating", "visits")


class RestaurantDetailSerializer(RestaurantListSerializer):
    visits = visit_serializers.VisitSerializer(many=True, read_only=True)
