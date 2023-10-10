from rest_framework import viewsets
from .serializers import (
    CargoSerializer,
    CargoRetrieveSerializer,
    CargoListSerializer,
    TruckSerializer,
)
from .models import Cargo, Truck
from django_filters import rest_framework as filters


class CargoFilter(filters.FilterSet):
    class Meta:
        model = Cargo
        fields = {
           'weight': ['lt', 'gt'],
        }


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.select_related('pickup_location', 'delivery_location').all()
    filterset_class = CargoFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return CargoListSerializer
        elif self.action == 'retrieve':
            return CargoRetrieveSerializer
        else:
            return CargoSerializer


class TruckViewSet(viewsets.ModelViewSet):
    serializer_class = TruckSerializer
    queryset = Truck.objects.select_related('location').all()
