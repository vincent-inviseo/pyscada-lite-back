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
    path("pages", PageApiView.as_view({'get': 'get_pages_by_building_id'})),
    path("pages/<int:page_id>/get", PageApiView.as_view({'get': 'retrieve'})),
    path("pages/create", PageApiView.as_view({'post': 'create'})),
    path("datas", FunctionsDatas.as_view({'get': 'get_data'})),
    path("charts", FunctionsDatas.as_view({'get': 'get_ids_charts_is_visible_page_id'})),
    path("background_data", FunctionsDatas.as_view({'get': 'get_data_background_all_devices'})),
    path("chart_date_range", FunctionsDatas.as_view({'get': 'get_value_by_chart_date_range'})),
]