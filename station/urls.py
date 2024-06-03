from rest_framework import routers

from station import views

app_name = "station"
router = routers.DefaultRouter()
router.register("stations", views.StationViewSet)
router.register("train-types", views.TrainTypeViewSet)
router.register("crews", views.CrewViewSet)
router.register("trains", views.TrainViewSet)
router.register("routes", views.RouteViewSet)
router.register("journeys", views.JourneyViewSet)
router.register("orders", views.OrderViewSet)
router.register("tickets", views.TicketViewSet)

urlpatterns = router.urls
