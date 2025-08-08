import pathlib
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError


class AirplaneType(models.Model):
    name = models.CharField(max_length=100)


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = models.CharField(max_length=100)


def airplane_image_path(instance, filename):
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix
    return pathlib.Path("upload/airplanes/") / pathlib.Path(filename)


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=airplane_image_path)


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="source_route")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="destination_route")
    distance = models.IntegerField()


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name='crew')


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["row", "seat", "flight"], name="unique_ticket_seat_flight")
        ]

    def clean(self):
        if self.flight and self.flight.airplane:
            max_rows = self.flight.airplane.rows
            max_seats = self.flight.airplane.seats_in_row

            errors = {}
            if not (1 <= self.row <= max_rows):
                errors["row"] = f"Row must be in range [1, {max_rows}]"
            if not (1 <= self.seat <= max_seats):
                errors["seat"] = f"Seat must be in range [1, {max_seats}]"

            if errors:
                raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
