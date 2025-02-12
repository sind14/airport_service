from rest_framework import viewsets
from airport.models import (
    Crew,
    Airplane,
    Airport,
    AirplaneType,
    Route, Flight,
)
from airport.serializers import (
    CrewListSerializer,
    AirplaneListSerializer,
    AirportListSerializer,
    AirplaneTypeListSerializer,
    RouteListSerializer,
    FlightListSerializer, FlightCreateSerializer, FlightDetailSerializer,
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewListSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneListSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportListSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeListSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteListSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightCreateSerializer
