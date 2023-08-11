from datetime import datetime, timedelta
from sched import scheduler
import requests
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from buildings.models import Building, Page, Chart, Device, Variable, VariableValues
from buildings.serializers import (
    BuildingReadSerializer,
    PageReadSerializer,
    ChartReadSerializer,
    DeviceReadSerializer,
    VariableReadSerializer,
    VariableValueReadSerializer
)
from webService.models import WebService
from webService.serializers import WebServiceSerializer

from .permissions import IsAuthorOrReadOnly

class BuildingApiView(viewsets.ViewSet):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def list(self, request):
        '''
        List all the todo items for given requested user
        '''
        buildings = Building.objects.all()
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
        building = Building.objects.get(pk=building_id)
        if not building:
            return Response({
                'res': "Building not exists"
            })
        try:
            serializer = BuildingReadSerializer(
                    building
                    )
            return Response(
                serializer.data
            )
        except Building.DoesNotExist:
            return None
        
    # 4. Update
    def get_object(self, request, building_id):
        '''
        Updates the todo item with given todo_id if exists
        '''
        building_instance = Building.objects.get(pk=building_id)
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
    
    
    def destroy(self, request, building_id):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        building_instance = Building.objects.get(pk=building_id)
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
    

class PageApiView(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def list(self, request):
        '''
        List all the todo items for given requested user
        '''
        pages = Page.objects.all()
        serializer = PageReadSerializer(pages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def create(self, request):
        '''
        Create the Todo with given todo data
        '''
        serializer = PageReadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = request.data
            Page.objects.create(
                name=data['name'],
                address=data['address'],
                createdAt=data['createdAt'],
                updatedAt=data['updatedAt'],
                position=data['position']
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, building_id):
        building = Building.objects.get(pk=building_id)
        if not building:
            return Response({
                'res': "Building not exists"
            })
        try:
            serializer = BuildingReadSerializer(
                    building
                    )
            return Response(
                serializer.data
            )
        except Building.DoesNotExist:
            return None
        
    # 4. Update
    def get_object(self, request, building_id):
        '''
        Updates the todo item with given todo_id if exists
        '''
        building_instance = Building.objects.get(pk=building_id)
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
    
    
    def destroy(self, request, building_id):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        building_instance = Building.objects.get(pk=building_id)
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
    
class FunctionsDatas(viewsets.ViewSet):
    def get_data(self, request):
        '''Get values from variables charts'''
        today = datetime.now()
        weekday = 6
        days = today.isoweekday() - weekday
        if days<0:
            days += 7
        previous_date = today - timedelta(days=days)
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        chart_id = request.GET.get('chart_id')
        chart = Chart.objects.get(pk=chart_id)
        serializer = ChartReadSerializer(
            chart
        )
        datas = {}
        variables = chart.variables
        if len(variables.all()) >= 1:
            for variable in variables.all():
                variable_value_serialized = {}
                for variable_value in VariableValues.objects.filter(variable=variable):
                    serializer = VariableValueReadSerializer(
                        variable_value
                    )
                    variable_value_serialized.update(serializer.data)
                    
                json_to_add = {
                    'name': variable.name,
                    'id': variable.id,
                    'values': variable_value_serialized
                }
                datas.update(json_to_add)
            
            
        return Response({'chart': serializer.data, 'datas': datas })
    
    def get_data_background_all_devices(self, request):
        '''Get all devices variables values and saves it'''
        variables = {}
        for device in Device.objects.all():
            '''If protocole is webservice'''
            #if device.protocol == 1:
            response_data = get_json_from_url(device.address)
            for variable in device.variables.all():
                webService = WebService.objects.filter(variable=variable).first()
                if webService:
                    serializer = VariableReadSerializer(
                        variable
                    )
                    variables.update(serializer.data)
                    save_variable_value(variable.id, response_data[webService.path])  
        return Response(variables)  


def save_variable_value(variable_id, value):
    value_saved = VariableValues.objects.create(recordedAt=datetime.now(), value=value)
    Variable.objects.update(id=variable_id ,values=value_saved)
    

    
def get_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lève une exception si la réponse contient un code d'erreur HTTP
        json_data = response.json()  # Convertit la réponse en objet JSON
        return json_data
    except requests.exceptions.RequestException as e:
        print("Une erreur s'est produite lors de la requête :", e)
        return None
    except ValueError as e:
            print("Erreur de décodage JSON :", e)
    return None
    