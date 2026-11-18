
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from weather.models import WeatherRecord
from weather.services.exceptions import (
    CityNotFoundError,
    OpenWeatherServiceError,
)


class WeatherCollectTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/weather/collect/"

    @patch("weather.views.OpenWeatherService")
    def test_collect_weather_success(self, mock_service):
        mock_weather_data = {
            "name": "Florianópolis",
            "sys": {"country": "BR"},
            "main": {
                "temp": 25.5,
                "feels_like": 26.0,
                "humidity": 80,
                "pressure": 1013,
            },
            "wind": {"speed": 5.2},
            "weather": [{"description": "céu limpo"}],
            "dt": 1795000000,
        }

        mock_service.return_value.get_weather.return_value = mock_weather_data

        mock_parsed_data = {
            "city": "Florianópolis",
            "country": "BR",
            "temperature": 25.5,
            "feels_like": 26.0,
            "humidity": 80,
            "pressure": 1013,
            "wind_speed": 5.2,
            "description": "céu limpo",
            "observed_at": "2026-11-18T12:00:00Z",
        }

        mock_service.return_value.parse_weather_data.return_value = mock_parsed_data

        response = self.client.post(
            self.url,
            {"city": "Florianópolis"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["city"], "Florianópolis")
        self.assertEqual(WeatherRecord.objects.count(), 1)

    @patch("weather.views.OpenWeatherService")
    def test_collect_weather_city_not_found(self, mock_service):
        mock_service.return_value.get_weather.side_effect = CityNotFoundError(
            'Cidade "CidadeInexistente" não encontrada.'
        )

        response = self.client.post(
            self.url,
            {"city": "CidadeInexistente"},
            format="json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(WeatherRecord.objects.count(), 0)

    @patch("weather.views.OpenWeatherService")
    def test_collect_weather_service_unavailable(self, mock_service):
        mock_service.return_value.get_weather.side_effect = (
            OpenWeatherServiceError("Falha na comunicação com a OpenWeather.")
        )

        response = self.client.post(
            self.url,
            {"city": "Florianópolis"},
            format="json",
        )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(WeatherRecord.objects.count(), 0)

    def test_list_weather_records(self):
        WeatherRecord.objects.create(
            city="Florianópolis",
            country="BR",
            temperature=25.5,
            feels_like=26.0,
            humidity=80,
            pressure=1013,
            wind_speed=5.2,
            description="céu limpo",
            observed_at="2026-11-18T12:00:00Z",
        )

        response = self.client.get("/api/weather/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["city"], "Florianópolis")

    def test_filter_weather_records_by_city(self):
        WeatherRecord.objects.create(
            city="Florianópolis",
            country="BR",
            temperature=25.5,
            feels_like=26.0,
            humidity=80,
            pressure=1013,
            wind_speed=5.2,
            description="céu limpo",
            observed_at="2026-11-18T12:00:00Z",
        )

        WeatherRecord.objects.create(
            city="São Paulo",
            country="BR",
            temperature=22.0,
            feels_like=22.5,
            humidity=70,
            pressure=1015,
            wind_speed=3.0,
            description="nublado",
            observed_at="2026-11-18T12:00:00Z",
        )

        response = self.client.get("/api/weather/?city=Florianópolis")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["city"], "Florianópolis")
