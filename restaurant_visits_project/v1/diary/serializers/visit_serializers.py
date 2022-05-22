from rest_framework import serializers

from v1.diary.models import Visit

BASE_FIELDS = ("id", "date", "bill", "notes", "rating")


class BaseVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = BASE_FIELDS


class VisitSerializer(BaseVisitSerializer):
    creator = serializers.HiddenField(default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()))

    class Meta:
        model = Visit
        fields = BASE_FIELDS + ("restaurant", "creator")
