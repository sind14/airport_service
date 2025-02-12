from rest_framework import serializers
from airport.models import (
    Airport,
    AirplaneType,
    Airplane,
    Crew,
    Order,
    Route,
    Flight,
    Ticket
)


class AirplaneTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ["id", "name"]


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = serializers.CharField(source="airplane_type.name")
    class Meta:
        model = Airplane
        fields = ["id", "name", "rows", "seats_in_row", "airplane_type"]


class CrewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ["id", "first_name", "last_name"]


class AirportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ["id", "name", "closest_big_city"]


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.closest_big_city")
    destination = serializers.CharField(source="destination.closest_big_city")
    class Meta:
        model = Route
        fields = ["id", "source", "destination", "distance"]


class FlightListSerializer(serializers.ModelSerializer):
    crew = CrewListSerializer(many=True)
    class Meta:
        model = Flight
        fields = ["id", "route", "airplane", "departure_time", "arrival_time", "crew"]


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "created_at", "user"]


class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "flight", "order"]