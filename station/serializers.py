from django.db import transaction
from rest_framework import serializers

from station.models import (
    TrainType,
    Station,
    Crew,
    Train,
    Route,
    Journey,
    Order,
    Ticket,
)


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = "__all__"


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class CrewSerializer(serializers.ModelSerializer):
    full_name = serializers.StringRelatedField(
        source="__str__",
        read_only=True,
    )

    class Meta:
        model = Crew
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = "__all__"


class TrainListSerializer(serializers.ModelSerializer):
    train_type = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = Train
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"

    def validate(self, attrs):
        Route.validate_source_destination(
            attrs["source"],
            attrs["destination"],
            serializers.ValidationError
        )
        return attrs


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    destination = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = Route
        fields = "__all__"


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = "__all__"


class JourneyListSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    train = TrainSerializer(read_only=True)

    class Meta:
        model = Journey
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "journey")

    def validate(self, attrs):
        Ticket.validate_seat(
            cargo=attrs["cargo"],
            seat=attrs["seat"],
            train_cargo_num=attrs["journey"].train.cargo_num,
            train_places_in_cargo=attrs["journey"].train.places_in_cargo,
            error_to_raise=serializers.ValidationError
        )
        return attrs


class TicketListSerializer(serializers.ModelSerializer):
    journey = JourneyListSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "journey")


class TicketForOrderSerializer(serializers.ModelSerializer):
    journey = serializers.StringRelatedField(
        read_only=True,
        source="journey.route.__str__",
    )

    class Meta:
        model = Ticket
        fields = ("id", "journey", "cargo", "seat")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket in tickets_data:
                Ticket.objects.create(order=order, **ticket)
            return order


class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    tickets = TicketForOrderSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
