from rest_framework.generics import ListAPIView

from .models import WeatherRecord 
from .serializers import WeatherRecordSerializer

class WeatherRecordListView(ListAPIView):
    queryset = WeatherRecord.objects.all()
    serializer_class = WeatherRecordSerializer

    def get_queryset(self):
      queryset =  WeatherRecord.objects.all()
      city = self.request.query_params.get('city')

      if city:
         queryset = queryset.filter(city__icontains=city)

      return queryset