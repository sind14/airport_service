from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from airport.models import (
    Crew,
    Airplane,
    Airport,
    AirplaneType,
    Route, Flight,
)
from airport.permissions import IsStuffOrReadOnly, IsAdminOrStuffReadOnly
from airport.serializers import (
    CrewListSerializer,
    AirplaneListSerializer,
    AirportListSerializer,
    AirplaneTypeListSerializer,
    RouteListSerializer,
    FlightListSerializer,
    FlightCreateSerializer,
    FlightDetailSerializer,
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrStuffReadOnly,)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrStuffReadOnly,)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrStuffReadOnly,)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrStuffReadOnly,)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = RouteListSerializer
    permission_classes = (IsAdminOrStuffReadOnly,)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsStuffOrReadOnly,)
    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightCreateSerializer
