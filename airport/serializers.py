from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from airport.models import (
    Airport,
    AirplaneType,
    Airplane,
    Crew,
    Order,
    Route,
    Flight,
    Ticket,
)


class AirplaneTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ["name"]


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(queryset=AirplaneType.objects.all(), slug_field="name")


    class Meta:
        model = Airplane
        fields = ["id", "name", "rows", "seats_in_row", "airplane_type", "image"]


class AirplaneImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ["id", "image"]


class CrewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ["first_name", "last_name"]


class AirportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ["name", "closest_big_city"]


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(queryset=Airport.objects.all(), slug_field="name")
    destination = serializers.SlugRelatedField(queryset=Airport.objects.all(), slug_field="name")
    class Meta:
        model = Route
        fields = ["source", "destination", "distance"]


class FlightListSerializer(serializers.ModelSerializer):
    route = RouteListSerializer()
    crew = CrewListSerializer(many=True)
    airplane = serializers.CharField(source="airplane.name")
    departure_time = serializers.DateTimeField()
    class Meta:
        model = Flight
        fields = ["id", "airplane", "route", "departure_time", "arrival_time", "crew"]


class FlightCreateSerializer(serializers.ModelSerializer):
    crew = serializers.PrimaryKeyRelatedField(queryset=Crew.objects.all(), many=True)
    departure_time = serializers.DateTimeField()
    arrival_time = serializers.DateTimeField()
    class Meta:
        model = Flight
        fields = ["route", "airplane", "departure_time", "arrival_time", "crew"]


class FlightDetailSerializer(serializers.ModelSerializer):
    airplane = AirplaneListSerializer()
    route = RouteListSerializer()
    crew = CrewListSerializer(many=True)
    class Meta:
        model = Flight
        fields = ["id", "airplane", "route", "departure_time", "arrival_time", "crew"]


class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "flight"]
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(),
                fields=("row", "seat", "flight")
            )
        ]


class OrderListSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(many=True, read_only=False, allow_empty=False)
    class Meta:
        model = Order
        fields = ["id", "created_at", "tickets"]

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order
