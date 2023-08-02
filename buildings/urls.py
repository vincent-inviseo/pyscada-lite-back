from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BuildingViewSet, ChartViewSet, DeviceViewApi, PageViewSet

app_name = "posts"

router = DefaultRouter()
router.register(r"buildings", BuildingViewSet)
router.register(r"pages", PageViewSet)
router.register(r"charts", ChartViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("devices/<int:pk>/", DeviceViewApi.as_view(), name="device"),
]