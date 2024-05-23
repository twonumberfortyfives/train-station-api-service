from rest_framework import viewsets

from station.models import (
    TrainType,
    Station,
    Crew,
    Journey,
    Order,
    Ticket,
    Route,
    Train
)
from station.serializers import (
    TrainTypeSerializer,
    StationSerializer,
    CrewSerializer,
    RouteSerializer,
    JourneySerializer,
    OrderSerializer,
    TicketSerializer,
    TrainSerializer,
    JourneyListSerializer,
    OrderListSerializer,
    TicketListSerializer,
    RouteListSerializer,
    TrainListSerializer
)


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ('list', 'retrieve'):
            queryset = queryset.select_related()
            return queryset
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TrainListSerializer
        return TrainSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ('list', 'retrieve'):
            queryset = queryset.select_related(
                "source",
                "destination"
            )
            return queryset
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RouteListSerializer
        return RouteSerializer


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ('list', 'retrieve'):
            queryset = queryset.select_related(
                "route",
                "train"
            ).prefetch_related(
                "route__source",
                "route__destination",
                "train__train_type"
            )
            return queryset
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return JourneyListSerializer
        return JourneySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ('list', 'retrieve'):
            queryset = queryset.select_related(
                "user"
            ).prefetch_related(
                "tickets__journey__route",
            )
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return OrderListSerializer
        return OrderSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ('list', 'retrieve'):
            queryset = queryset.select_related(
                "journey",
                "order"
            )
            queryset = queryset.prefetch_related(
                "journey__route__destination",
                "journey__train__train_type",
            )
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TicketListSerializer
        return TicketSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
