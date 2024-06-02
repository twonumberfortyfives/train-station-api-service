from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

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
    TrainListSerializer, ImageTrainSerializer
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
            queryset = queryset.filter(name__icontains=name)
        if train_type:
            queryset = queryset.filter(train_type__name__icontains=train_type)
        if self.action in ('list', 'retrieve'):
            return queryset
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TrainListSerializer
        elif self.action == "upload_image":
            return ImageTrainSerializer
        return TrainSerializer

    @action(
        methods=['POST'],
        detail=True,
        url_path='upload-image',
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        train = self.get_object()
        serializer = ImageTrainSerializer(train, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "train type",
                type={"type": "array", "items": {"type": "string"}},
                description="filtering by train type name"
                            "ex(?train_type=Express)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request)


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
            queryset = queryset.filter(source__name__icontains=source)
        elif destination:
            queryset = queryset.filter(destination__name__icontains=destination)
        elif source and destination:
            queryset = queryset.filter(source__name__icontains=source, destination__name__icontains=destination)
        if self.action in ('list', 'retrieve'):
            return queryset
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RouteListSerializer
        return RouteSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source/destination",
                type={"type": "array", "items": {"type": "string"}},
                description="filtering by source or destination or both"
                            "ex(?source=Kyiv&?destination=Lviv)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request)


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
            queryset = queryset.filter(departure_time__icontains=departure_time)
        elif arrival_time:
            queryset = queryset.filter(arrival_time__icontains=arrival_time)
        if self.action in ('list', 'retrieve'):
            return queryset
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return JourneyListSerializer
        return JourneySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "departure_time/arrival_time",
                type={"type": "array", "items": {"type": "string"}},
                description="filtering by departure/arrival time "
                            "ex(?departure_time=2010-10-12../?arrival_time=2012-10-2)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
            return super().list(request)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ('list', 'retrieve'):
            if self.request.user.is_authenticated and not self.request.user.is_staff:
                queryset = queryset.filter(user=self.request.user)
            else:
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
