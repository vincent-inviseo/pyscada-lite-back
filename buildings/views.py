import json
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

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

class BuildingApiView(viewsets.ViewSet):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def list(self, request):
        '''
        List all the todo items for given requested user
        '''
        buildings = Building.objects.filter(user = request.user.id)
        serializer = BuildingReadSerializer(buildings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def create(self, request):
        '''
        Create the Todo with given todo data
        '''
        serializer = BuildingReadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = request.data
            Building.objects.create(
                name=data['name'],
                address=data['address'],
                createdAt=data['createdAt'],
                updatedAt=data['updatedAt'],
                position=data['position']
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, building_id):
        try:
            serializer = BuildingReadSerializer(
                    Building.objects.get(id=building_id)
                    )
            return Response(
                serializer.data
            )
        except Building.DoesNotExist:
            return None
        
    # 4. Update
    def update(self, request, building_id):
        '''
        Updates the todo item with given todo_id if exists
        '''
        building_instance = self.get_object(building_id, request.user.id)
        if not building_instance:
            return Response(
                {"res": "Object with building id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = BuildingReadSerializer(instance = building_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def destroy(self, request, building_id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        building_instance = self.get_object(building_id, request.user.id)
        if not building_instance:
            return Response(
                {"res": "Object with building id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        building_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    

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
class DeviceViewSet(viewsets.ModelViewSet):

    queryset = Device.objects.all()
    
    def get_queryset(self):
        res = super().get_queryset()
        variable_id = self.kwargs.get("variable_id")
        return res.filter(variable__id=variable_id)

    def get_serializer_class(self):
        return DeviceReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()