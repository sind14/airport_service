from django.urls import path, include
from rest_framework import routers
from airport.views import CrewViewSet, AirplaneViewSet, AirportViewSet

router = routers.DefaultRouter()
router.register("crew_list", CrewViewSet)
router.register("airplane_list", AirplaneViewSet)
router.register("airport_list", AirportViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
