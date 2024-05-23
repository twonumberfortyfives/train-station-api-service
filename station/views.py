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
        queryset = self.queryset.select_related()
        name = self.request.query_params.get('name')
        train_type = self.request.query_params.get('train_type')
        if name:
            return queryset.filter(name__icontains=name)
        if train_type:
            return queryset.filter(train_type__name__icontains=train_type)
        if self.action in ('list', 'retrieve'):
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
        queryset = self.queryset.select_related(
                "source",
                "destination"
            )
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        if source:
            return queryset.filter(source__name__icontains=source)
        elif destination:
            return queryset.filter(destination__name__icontains=destination)
        elif source and destination:
            return queryset.filter(source__name__icontains=source, destination__name__icontains=destination)
        if self.action in ('list', 'retrieve'):
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
        queryset = self.queryset.select_related(
                "route",
                "train"
            ).prefetch_related(
                "route__source",
                "route__destination",
                "train__train_type"
            )
        departure_time = self.request.query_params.get("departure_time")
        arrival_time = self.request.query_params.get("arrival_time")
        if departure_time:
            return queryset.filter(departure_time__icontains=departure_time)
        elif arrival_time:
            return queryset.filter(arrival_time__icontains=arrival_time)
        if self.action in ('list', 'retrieve'):
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
