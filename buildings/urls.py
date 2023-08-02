from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BuildingViewSet, ChartViewSet, DeviceViewSet, PageViewSet

app_name = "posts"

router = DefaultRouter()
router.register(r"buildings", BuildingViewSet)
router.register(r"pages", PageViewSet)
router.register(r"charts", ChartViewSet)
router.register(r"devices", DeviceViewSet)

urlpatterns = [
    path("", include(router.urls))
]