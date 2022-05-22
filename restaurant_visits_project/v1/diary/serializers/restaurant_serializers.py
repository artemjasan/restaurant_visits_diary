from rest_framework import serializers

from v1.diary.models import Restaurant, Visit


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ("id", "date", "bill", "notes", "rating", "restaurant")


class RestaurantListSerializer(serializers.ModelSerializer):

    visits = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    creator = serializers.HiddenField(default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()))

    class Meta:
        model = Restaurant
        fields = ("id", "name", "city", "cuisine", "visits", "creator")


class RestaurantDetailSerializer(RestaurantListSerializer):

    visits = VisitSerializer(many=True, read_only=True)

