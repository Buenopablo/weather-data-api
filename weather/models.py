from django.db import models


# Create your models here.
class WeatherRecord(models.Model):
    city = models.CharField(max_length=100, db_index=True)
    country = models.CharField(max_length=2)
    temperature = models.DecimalField(max_digits=7, decimal_places=2)
    feels_like = models.DecimalField(max_digits=7, decimal_places=2)
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    wind_speed = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=255)
    observed_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city}, {self.country} - {self.observed_at}"
