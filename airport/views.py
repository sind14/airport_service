from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from airport.models import (
    Crew,
    Airplane,
    Airport,
    AirplaneType,
    Route, Flight, Order,
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
    AirplaneImageSerializer, OrderListSerializer,
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

    def get_serializer_class(self):
        if self.action == "upload_image":
            return AirplaneImageSerializer
        return AirplaneListSerializer


    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminOrStuffReadOnly],
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        airplane = self.get_object()
        serializer = self.get_serializer(airplane, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
