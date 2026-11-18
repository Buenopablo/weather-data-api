from rest_framework.generics import ListAPIView

from .models import WeatherRecord
from .serializers import WeatherRecordSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .services.openweather import OpenWeatherService
from .services.exceptions import (
    CityNotFoundError,
    OpenWeatherAuthenticationError,
    OpenWeatherServiceError,
)


class WeatherRecordListView(ListAPIView):
    queryset = WeatherRecord.objects.all()
    serializer_class = WeatherRecordSerializer

    def get_queryset(self):
        queryset = WeatherRecord.objects.all()
        city = self.request.query_params.get("city")

        if city:
            queryset = queryset.filter(city__icontains=city)

        return queryset


class WeatherRecordCollectView(APIView):
    def post(self, request):
        city = request.data.get("city")

        if not isinstance(city, str) or not city.strip():
            raise ValidationError({"city": "Informe um nome de cidade válido."})

        city = city.strip()

        openweather_service = OpenWeatherService()

        try:
            weather_data = openweather_service.get_weather(city)
            parsed_data = openweather_service.parse_weather_data(weather_data)

            serializer = WeatherRecordSerializer(data=parsed_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except CityNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except OpenWeatherAuthenticationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        except OpenWeatherServiceError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
