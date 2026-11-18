from datetime import datetime, timezone
import requests
from decouple import config
from requests.exceptions import RequestException, Timeout
from .exceptions import (
    CityNotFoundError,
    OpenWeatherAuthenticationError,
    OpenWeatherServiceError,
)


class OpenWeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self.api_key = config("OPENWEATHER_API_KEY")

    def get_weather(self, city):
        params = {"q": city, "appid": self.api_key, "units": "metric", "lang": "pt_br"}

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)

            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise CityNotFoundError(f'Cidade "{city}" não encontrada.') from error

            elif error.response.status_code == 401:
                raise OpenWeatherAuthenticationError(
                    "Erro de autenticação com a OpenWeather."
                ) from error
            elif error.response.status_code == 429:
                raise OpenWeatherServiceError(
                    "Limite de requisições atingido na OpenWeather."
                ) from error
            else:
                raise OpenWeatherServiceError(
                    "Erro ao consultar a OpenWeather."
                ) from error

        except Timeout as error:
            raise OpenWeatherServiceError(
                "Tempo limite excedido ao consultar a OpenWeather."
            ) from error

        except RequestException as error:
            raise OpenWeatherServiceError(
                "Falha na comunicação com a OpenWeather."
            ) from error

    def parse_weather_data(self, data):
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"],
            "observed_at": datetime.fromtimestamp(data["dt"], tz=timezone.utc),
        }
