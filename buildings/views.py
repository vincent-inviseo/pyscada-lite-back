from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from buildings.models import Building, Page, Chart, Device, Variable, AlertVariable
from buildings.serializers import (
    BuildingReadSerializer,
    PageReadSerializer,
    ChartReadSerializer,
    DeviceReadSerializer,
    VariableReadSerializer,
    AlertVariableReadSerializer
)

from .permissions import IsAuthorOrReadOnly

class BuildingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and Retrieve post categories
    """

    queryset = Building.objects.all()
    serializer_class = BuildingReadSerializer
    permission_classes = (permissions.AllowAny,)

class PageViewSet(viewsets.ModelViewSet):

    queryset = Page.objects.all()
    
    def get_serializer_class(self):
        return PageReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()

class ChartViewSet(viewsets.ModelViewSet):

    queryset = Chart.objects.all()

    def get_queryset(self):
        res = super().get_queryset()
        page_id = self.kwargs.get("page_id")
        return res.filter(page__id=page_id)

    def get_serializer_class(self):
        return ChartReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()

# Here, we are using the normal APIView class
class DeviceViewApi(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        user = request.user
        device = get_object_or_404(Device, pk=pk)

        return Response(status=status.HTTP_200_OK)