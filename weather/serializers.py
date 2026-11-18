from rest_framework import serializers
from .models import WeatherRecord


class WeatherRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherRecord
        fields = "__all__"


class WeatherCollectSerializer(serializers.Serializer):
    city = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100,
    )