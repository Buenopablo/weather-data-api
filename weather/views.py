from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from django.contrib.postgres.lookups import Unaccent
from django.db.models import CharField

from .models import WeatherRecord
from .serializers import WeatherCollectSerializer, WeatherRecordSerializer

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

CharField.register_lookup(Unaccent)

@extend_schema(
    parameters=[
        OpenApiParameter(
            name="city",
            description="Filtra os registros pelo nome da cidade.",
            required=False,
            type=str,
        ),
    ],
    responses=WeatherRecordSerializer(many=True),
    description="Lista os registros meteorológicos, permitindo filtrar por cidade.",
)

class WeatherRecordListView(ListAPIView):
    queryset = WeatherRecord.objects.all()
    serializer_class = WeatherRecordSerializer

    def get_queryset(self):
        queryset = WeatherRecord.objects.all()
        city = self.request.query_params.get("city")

        if city:
            queryset = queryset.filter(city__unaccent__icontains=city)

        return queryset


class WeatherRecordCollectView(APIView):
    @extend_schema(
        request=WeatherCollectSerializer,
        responses={
            201: WeatherRecordSerializer,
        },
        description="Consulta a OpenWeather e armazena os dados meteorológicos da cidade.",
    )
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
