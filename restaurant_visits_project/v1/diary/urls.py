from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import VisitsViewSet, RestaurantsViewSet

router = SimpleRouter()

router.register(r"restaurants", RestaurantsViewSet, basename="restaurant")
router.register(r"visits", VisitsViewSet, basename="visit")

urlpatterns = [path("", include(router.urls))]
