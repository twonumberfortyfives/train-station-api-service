from django.contrib.admin import ModelAdmin, register
from .models import (
    TrainType,
    Station,
    Crew,
    Train,
    Route,
    Journey,
    Order,
    Ticket
)


@register(TrainType)
class TrainTypeAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@register(Station)
class StationAdmin(ModelAdmin):
    list_display = ("name", "latitude", "longitude")
    search_fields = ("name",)


@register(Crew)
class CrewAdmin(ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")


@register(Train)
class TrainAdmin(ModelAdmin):
    list_display = (
        "name",
        "cargo_num",
        "places_in_cargo",
        "train_type",
        "capacity"
    )
    search_fields = ("name",)
    list_filter = ("train_type",)
    ordering = ("name",)


@register(Route)
class RouteAdmin(ModelAdmin):
    list_display = ("source", "destination", "distance")
    search_fields = ("source__name", "destination__name")
    list_filter = ("source", "destination")
    ordering = ("source", "destination")


@register(Journey)
class JourneyAdmin(ModelAdmin):
    list_display = ("route", "train", "departure_time", "arrival_time")
    search_fields = (
        "route__source__name",
        "route__destination__name",
        "train__name"
    )
    list_filter = ("departure_time", "arrival_time")
    ordering = ("departure_time",)


@register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ("created_at", "user")
    search_fields = ("user__username",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@register(Ticket)
class TicketAdmin(ModelAdmin):
    list_display = ("cargo", "seat", "journey", "order")
    search_fields = (
        "journey__route__source__name",
        "journey__route__destination__name",
        "journey__train__name",
        "order__user__username",
    )
    list_filter = ("journey__departure_time", "journey__arrival_time")
    ordering = ("journey__departure_time",)
