from django.contrib import admin
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


@admin.register(TrainType)
class TrainTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude")
    search_fields = ("name",)


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
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


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("source", "destination", "distance")
    search_fields = ("source__name", "destination__name")
    list_filter = ("source", "destination")
    ordering = ("source", "destination")


@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ("route", "train", "departure_time", "arrival_time")
    search_fields = (
        "route__source__name",
        "route__destination__name",
        "train__name"
    )
    list_filter = ("departure_time", "arrival_time")
    ordering = ("departure_time",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user")
    search_fields = ("user__username",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("cargo", "seat", "journey", "order")
    search_fields = (
        "journey__route__source__name",
        "journey__route__destination__name",
        "journey__train__name",
        "order__user__username",
    )
    list_filter = ("journey__departure_time", "journey__arrival_time")
    ordering = ("journey__departure_time",)
