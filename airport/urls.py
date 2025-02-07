from django.urls import path, include
from rest_framework import routers
from airport.views import CrewViewSet, AirplaneViewSet

router = routers.DefaultRouter()
router.register("crew_list", CrewViewSet)
router.register("airplane_list", AirplaneViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
