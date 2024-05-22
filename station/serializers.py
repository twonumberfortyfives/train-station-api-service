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
        models = TrainType
        fields = "__all__"


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        models = Station
        fields = "__all__"


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        models = Crew
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        models = Train
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        models = Route
        fields = "__all__"


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        models = Journey
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        models = Order
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        models = Ticket
        fields = "__all__"
