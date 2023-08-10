from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BuildingApiView, FunctionsDatas, PageApiView


urlpatterns = [
    path("buildings/", BuildingApiView.as_view({'get': 'list'})),
    path("pages/", PageApiView.as_view({'get': 'list'})),
    path("buildings/create", BuildingApiView.as_view({'post': 'create'})),
    path("buildings/<int:building_id>/get", BuildingApiView.as_view({'get': 'retrieve'})),
    path("buildings/<int:building_id>/update", BuildingApiView.as_view({'put': 'get_object'})),
    path("buildings/<int:building_id>/delete", BuildingApiView.as_view({'delete': 'destroy'})),
    path("datas", FunctionsDatas.as_view({'get': 'get_data'})),
    path("background_data", FunctionsDatas.as_view({'get': 'get_data_background_all_devices'}))
]