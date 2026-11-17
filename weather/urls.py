from django.urls import path
from .views import WeatherRecordListView

urlpatterns = [
    path('weather/', WeatherRecordListView.as_view(), name='weather-list'),
]