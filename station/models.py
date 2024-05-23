from django.db import models

from train_station_api_service import settings


class TrainType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=255)
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

    def __str__(self):
        return f"from ({self.source.name}) to ({self.destination.name}) distance: {self.distance}"


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
