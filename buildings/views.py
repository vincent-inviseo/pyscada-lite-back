from datetime import datetime, timedelta
import requests
import time
import schedule
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

    def get_pages_by_building_id(self, request):
        requested_building_id = request.GET.get('building_id')
        pages = Page.objects.filter(building_id=requested_building_id)
        json_pages = {'pages': []}
        if len(pages.all()) >= 1:
            for page in pages.all():
                serializer = PageReadSerializer(
                    page
                )
                json_pages['pages'].append(
                    serializer.data
                )

        return Response(json_pages)

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
        datas = {'variables': []}
        variables = chart.variables
        if len(variables.all()) >= 1:
            for variable in variables.all():
                variable_value_serialized = {}
                values = {'value': []}
                for variable_value in VariableValues.objects.filter(variable=variable):
                    serializer_value = VariableValueReadSerializer(
                        variable_value
                    )

                    values['value'].append({
                        'id': serializer_value.data['id'],
                        'recordedAt': serializer_value.data['recordedAt'],
                        'value': serializer_value.data['value']
                    })

                datas['variables'].append({
                    'name': variable.name,
                    'id': variable.id,
                    'values': values
                })
            
            
        return Response({'chart': serializer.data, 'datas': datas })
    
    def get_ids_charts_is_visible_page_id(self, request):
        '''Get the id of all visible charts'''
        is_visible = request.GET.get('is_visible')
        page_id = request.GET.get('page_id')
        charts = Chart.objects.filter(visible=is_visible).filter(pages=page_id).only('id')
        json_charts = {'charts_ids': []}
        if len(charts.all()) >= 1:
            for chart in charts.all():
                json_charts['charts_ids'].append(
                    chart.id
                )

        return Response(json_charts)
        
    
    @schedule.repeat(schedule.every(10).seconds)
    def get_data_background_all_devices(self, request):
        '''Get all devices variables values and saves it'''
        json_variables = {'variables': []}
        for device in Device.objects.all():
            '''If protocole is webservice'''
            #if device.protocol == 1:
            response_data = get_json_from_url(device.address)
            for variable in device.variables.all():
                print(variable)
                webService = WebService.objects.filter(variable=variable).first()
                print(webService)
                if webService:
                    serializer = VariableReadSerializer(
                        variable
                    )
                    json_variable = serializer.data
                    save_variable_value(variable.id, response_data[webService.path])  
                    values = VariableValues.objects.filter(variable=variable)
                    values_serialized = []
                    json_values = []
                    for value in values:
                        serializer_value = VariableValueReadSerializer(
                            value
                        )
                        json_values.append({
                            'id': serializer_value.data['id'],
                            'recordedAt': serializer_value.data['recordedAt'],
                            'value': serializer_value.data['value'],
                            'variable': serializer_value.data['variable']
                        })
                    json_variables['variables'].append({
                        'variable': json_variable,
                        'values': json_values
                    })
        return Response(json_variables)
        
def save_variable_value(variable_id, value):
    VariableValues.objects.create(recordedAt=datetime.now(), value=value, variable_id=variable_id)
    

    
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