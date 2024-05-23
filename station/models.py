from django.db import models
from rest_framework.exceptions import ValidationError

from train_station_api_service import settings


class TrainType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=255, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def __str__(self):
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Train(models.Model):
    name = models.CharField(max_length=255)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(TrainType, on_delete=models.CASCADE, related_name='trains')

    def __str__(self):
        return f"{self.name} ({self.train_type}) cargos: {self.cargo_num}, places in cargo: {self.places_in_cargo}"


class Route(models.Model):
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='routes_source')
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='routes_destination')
    distance = models.IntegerField()

    class Meta:
        unique_together = (('source', 'destination'),)
        indexes = [
            models.Index(fields=['source', 'destination']),
        ]

    def __str__(self):
        return f"from ({self.source.name}) to ({self.destination.name}) distance: {self.distance}"

    @staticmethod
    def validate_source_destination(source, destination, error_to_raise):
        if source == destination:
            raise error_to_raise(
                f"Source and destination can not be the same"
            )

    def clean(self):
        Route.validate_source_destination(self.source, self.destination, ValueError)

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.clean_fields()
        return super(Route, self).save(force_insert, force_update, using, update_fields)


class Journey(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='journeys')
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='journeys')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.route} {self.train} DEPARTURE: ({self.departure_time}), ARRIVAL: ({self.arrival_time})"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name='tickets')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
