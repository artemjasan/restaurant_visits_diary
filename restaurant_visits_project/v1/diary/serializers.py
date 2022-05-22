from rest_framework import serializers

from .models import Restaurant, Visit


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ("id", "date", "bill", "notes", "rating", "restaurant")


class RestaurantListSerializer(serializers.ModelSerializer):

    visits = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ("id", "name", "city", "cuisine", "visits")


class RestaurantDetailSerializer(RestaurantListSerializer):

    visits = VisitSerializer(many=True, read_only=True)

