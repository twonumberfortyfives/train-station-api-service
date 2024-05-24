from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

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
        validators = [
            UniqueTogetherValidator(
                queryset=Station.objects.all(),
                fields=("name", "latitude", "longitude"),
            )
        ]


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

    def validate(self, attrs):
        Train.validate_train(
            cargo_num=attrs["cargo_num"],
            places_in_cargo=attrs["places_in_cargo"],
            error_to_raise=serializers.ValidationError,
        )


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
        validators = [
            UniqueTogetherValidator(
                queryset=Route.objects.all(),
                fields=("source", "destination", "distance"),
            )
        ]

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
    route = RouteListSerializer(read_only=True)
    train = TrainSerializer(read_only=True)
    ticket_available = serializers.SerializerMethodField(
        method_name="get_ticket_available"
    )
    places_occupied = serializers.SerializerMethodField(
        method_name="get_places_occupied"
    )

    class Meta:
        model = Journey
        fields = "__all__"

    def get_ticket_available(self, obj):
        tickets_in_total = obj.tickets.count()
        all_places = obj.train.capacity
        return all_places - tickets_in_total

    def get_places_occupied(self, obj):
        return obj.tickets.count()


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "journey")
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(),
                fields=("cargo", "seat", "journey"),
            )
        ]

    def validate(self, attrs):
        Ticket.validate_seat(
            cargo=attrs["cargo"],
            seat=attrs["seat"],
            train_cargo_num=attrs["journey"].train.cargo_num,
            train_places_in_cargo=attrs["journey"].train.places_in_cargo,
            error_to_raise=serializers.ValidationError
        )
        return attrs


class JourneySerializerForTicketList(serializers.ModelSerializer):
    route = RouteListSerializer(read_only=True)
    train = TrainSerializer(read_only=True)

    class Meta:
        model = Journey
        fields = "__all__"


class TicketListSerializer(serializers.ModelSerializer):
    source = serializers.CharField(
        source="journey.route.source",
        read_only=True,
    )
    destination = serializers.CharField(
        source="journey.route.destination",
        read_only=True
    )
    train = serializers.CharField(
        source="journey.train.name",
    )
    train_type = serializers.CharField(
        source="journey.train.train_type",
    )
    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "source", "destination", "train", "train_type")


class TicketForOrderSerializer(serializers.ModelSerializer):
    journey = serializers.StringRelatedField(
        read_only=True,
        source="journey.route.__str__",
    )

    class Meta:
        model = Ticket
        fields = ("id", "journey", "cargo", "seat")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

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
