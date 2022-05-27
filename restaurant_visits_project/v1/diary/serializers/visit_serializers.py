import datetime
from rest_framework import serializers
from v1.diary.models import Visit

BASE_FIELDS = ("id", "date", "bill", "notes", "rating")


class BaseVisitSerializer(serializers.ModelSerializer):
    def validate_date(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError("the visit can't be in future")
        return value

    class Meta:
        model = Visit
        fields = BASE_FIELDS


class VisitSerializer(BaseVisitSerializer):
    creator = serializers.HiddenField(default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()))

    class Meta:
        model = Visit
        fields = BASE_FIELDS + ("restaurant", "creator")
