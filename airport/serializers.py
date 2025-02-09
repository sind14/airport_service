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


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ["id", "name"]


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.CharField(source="airplane_type.name")
    class Meta:
        model = Airplane
        fields = ["id", "name", "rows", "seats_in_row", "airplane_type"]


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ["id", "first_name", "last_name"]


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ["id", "name", "closest_big_city"]


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.closest_big_city")
    destination = serializers.CharField(source="destination.closest_big_city")
    class Meta:
        model = Route
        fields = ["id", "source", "destination", "distance"]

    def create(self, validated_data):
        source_city = validated_data.pop("source")["closest_big_city"]
        destination_city = validated_data.pop("destination")["closest_big_city"]
        source_airport = Airport.objects.get(closest_big_city=source_city)
        destination_airport = Airport.objects.get(closest_big_city=destination_city)
        route = Route.objects.create(
            source=source_airport,
            destination=destination_airport,
            **validated_data
        )

        return route


class FlightSerializer(serializers.ModelSerializer):
    crew = CrewSerializer(many=True)
    class Meta:
        model = Flight
        fields = ["id", "route", "airplane", "departure_time", "arrival_time", "crew"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "created_at", "user"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "flight", "order"]