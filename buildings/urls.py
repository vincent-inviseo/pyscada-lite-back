from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BuildingApiView


urlpatterns = [
    path("buildings/", BuildingApiView.as_view({'get': 'list'})),
    path("buildings/create", BuildingApiView.as_view({'post': 'create'})),
    path("buildings/<int:building_id>/get", BuildingApiView.as_view({'get': 'retrieve'})),
    path("buildings/<int:building_id>/update", BuildingApiView.as_view({'put': 'get_object'})),
]