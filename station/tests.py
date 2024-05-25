from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APIClient

from station.models import Train, TrainType, Journey, Route, Station, Order
from station.serializers import TrainListSerializer

STATIONS_URL = reverse("station:station-list")
TRAINS_URL = reverse("station:train-list")
ORDER_URL = reverse("station:order-list")


class TestUnauthenticatedUser(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_user(self):
        response = self.client.get(STATIONS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAuthenticatedUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="asjkdk@gmail.com",
            password="passwordS123",
        )
        self.client.force_authenticate(user=self.admin)
        self.train_type = TrainType.objects.create(
            name="Test train type",
        )
        self.train_type_2 = TrainType.objects.create(
            name="2",
        )
        self.train_1 = Train.objects.create(
            name="Test Train",
            cargo_num=4,
            places_in_cargo=25,
            train_type=self.train_type,
        )

        self.train_2 = Train.objects.create(
            name="2",
            cargo_num=4,
            places_in_cargo=25,
            train_type=self.train_type_2,
        )
        self.user = get_user_model().objects.create_user(
            email="email@gmail.com",
            password="<PASSWORD>123",
        )

    def test_authenticated_user(self):
        response = self.client.get(STATIONS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_train_list(self):
        response = self.client.get(TRAINS_URL)
        trains = Train.objects.all()
        serializer = TrainListSerializer(trains, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_train_detail(self):
        response = self.client.get(TRAINS_URL, {"name": f"{self.train_1.name}"})
        serializer = TrainListSerializer(self.train_1, many=False)
        print(serializer.data)
        print(response.data["results"])
        self.assertEqual(response.data["results"], [serializer.data])

    def test_train_filter_by_name(self):
        response = self.client.get(TRAINS_URL, {"name": self.train_1.name})
        serializer = TrainListSerializer(self.train_1, many=False)
        serializer_2 = TrainListSerializer(self.train_2, many=False)
        self.assertEqual(response.data["results"], [serializer.data])
        self.assertNotEqual(response.data["results"], [serializer_2.data])

    def test_train_filter_by_train_type(self):
        response = self.client.get(TRAINS_URL, {"train_type": self.train_1.train_type})
        serializer = TrainListSerializer(self.train_1, many=False)
        serializer_2 = TrainListSerializer(self.train_2, many=False)
        self.assertEqual(response.data["results"], [serializer.data])
        self.assertNotEqual(response.data["results"], [serializer_2.data])

    def test_train_forbidden(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "name": "test_train",
            "cargo_num": 4,
            "places_in_cargo": 21,
            "train_type": self.train_type,
        }
        response = self.client.post(TRAINS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_not_staff_can_make_order(self):
        self.client.force_authenticate(user=self.user)
        source = Station.objects.create(
            name="source_test",
            latitude=123,
            longitude=123,
        )
        destination = Station.objects.create(
            name="destination_test",
            latitude=123,
            longitude=123,
        )
        route = Route.objects.create(
            source=source,
            destination=destination,
            distance=123,
        )
        journey = Journey.objects.create(
            route=route,
            train=self.train_1,
            departure_time="2024-05-23 10:00:00",
            arrival_time="2024-06-23 10:00:00",
        )
        payload = {
            "tickets": [
                {
                    "journey": journey.id,
                    "cargo": 1,
                    "seat": 2,
                }
            ]
        }
        response = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
