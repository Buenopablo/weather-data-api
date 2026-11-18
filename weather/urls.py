from django.urls import path
from .views import WeatherRecordListView, WeatherRecordCollectView

urlpatterns = [
    path("weather/", WeatherRecordListView.as_view(), name="weather-list"),
    path(
        "weather/collect/",
        WeatherRecordCollectView.as_view(),
        name="weather-collect",
    ),
]
