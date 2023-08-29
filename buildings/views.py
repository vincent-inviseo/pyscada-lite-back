from datetime import datetime, timedelta
import json
from threading import Thread
from django.http import JsonResponse
import requests
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from buildings.enums.aggregation_types import AggregationType
from buildings.models import Building, Page, Chart, Device, Unit, Variable, VariableValues
from buildings.serializers import (
    BuildingReadSerializer,
    PageReadSerializer,
    ChartReadSerializer,
    DeviceReadSerializer,
    UnitReadSerializer,
    VariableReadSerializer,
    VariableValueReadSerializer
)
from webService.models import WebService
from asgiref.sync import sync_to_async

from .permissions import IsAuthorOrReadOnly
'''
globals variables
'''
values_aggregated = [] # values aggregated stored here

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


    def retrieve(self, request, page_id):
        page = Page.objects.get(pk=page_id)
        if not page:
            return Response({
                'res': "page not exists"
            })
        try:
            serializer = PageReadSerializer(
                    page
                    )
            return Response(
                serializer.data
            )
        except Page.DoesNotExist:
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

    def get_value_by_chart_date_range(selft, request):
        dateStart = request.GET.get('date_start')
        dateEnd = request.GET.get('date_end')
        chart_id = request.GET.get('chart_id')
        aggregate_type = None
        aggregate_type = request.GET.get('aggregate_type')
         
        chart = Chart.objects.get(pk=chart_id)
        variables = chart.variables
        response = []
        
        for variable in variables.all():
            valuesVariable = VariableValues.objects.filter(variable=variable)
            values = valuesVariable.filter(recordedAt__gte=dateStart, recordedAt__lte=dateEnd)
            json_values = []
            aggregate_type_list = [aggregate.value for aggregate in AggregationType]
            if not aggregate_type == None and int(aggregate_type) in aggregate_type_list:
                values_aggregated = aggregate_values_by_date_range(values, int(aggregate_type))
                for value in values_aggregated:
                    json_values.append(
                        value
                    )
                variable_part_response = {
                    'id': variable.id,
                    'unit': variable.unit.unit,
                    'name': variable.name,
                    'values': json_values
                }
                response.append(variable_part_response)
            else:
                for value in values:
                    serializer_value = VariableValueReadSerializer(
                        value
                    )
                    json_values.append({
                        'id': serializer_value.data['id'],
                        'recordedAt': serializer_value.data['recordedAt'],
                        'value': serializer_value.data['value']
                    })
                variable_part_response = {
                    'id': variable.id,
                    'unit': variable.unit.unit,
                    'name': variable.name,
                    'values': json_values
                }
                response.append(variable_part_response)
        return Response(response)


class VariableValuesView(viewsets.ViewSet):
    
    def import_variable_value(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            variable_id = data.get('variable_id')
            variable = Variable.objects.get(id=variable_id)
            if not variable:
                return JsonResponse("Variable not exist")
            value = data.get('value')
            recordedAt = data.get('recordedAt')
            VariableValues.objects.create(value=value, recordedAt=recordedAt, variable_id= variable.id)
            return JsonResponse("Variable value created")
        
class VariableView(viewsets.ViewSet):
    
    def create(self, request):
        variable = {}
        if request.method == 'POST':
            data = json.loads(request.body)
            unit_unit = data.get('unit_unit')
            unit_description = data.get('unit_description')
            unit_udunit = data.get('unit_udunit')
            name = data.get('name')
            description = data.get('description')
            createdAt = datetime.now()
            updatedAt = datetime.now()
            data_type = data.get('data_type')
            unit = Unit.objects.create(unit=unit_unit,
                                       description=unit_description,
                                       udunit=unit_udunit)
            variable = Variable.objects.create(name=name,
                                               description=description,
                                               createdAt=createdAt,
                                               updatedAt=updatedAt,
                                               value_class=data_type,
                                               unit=unit)
        serializer_unit = UnitReadSerializer(
            unit
        )
        serialize_variable = VariableReadSerializer(
            variable
        )
        return JsonResponse({'variable':serialize_variable.data, 'unit': serializer_unit.data})
            
            
    
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

def save_variable_value(variable_id, value):
    VariableValues.objects.create(recordedAt=datetime.now(), value=value, variable_id=variable_id)
    

def aggregate_values_by_date_range(values, aggregate_type):
    result = []
    
    '''
    aggregate by minute
    '''
    if aggregate_type == 1:
        # Convertir la liste d'objets en un dictionnaire avec recordedAt comme clé
        objects_dict = {obj.recordedAt: obj for obj in values}

        start_date = min(objects_dict.keys())
        end_date = max(objects_dict.keys())

        current_date = start_date
        while current_date <= end_date:
            next_date = current_date + timedelta(minutes=1)

            # Sélectionner les objets enregistrés entre current_date et next_date
            filtered_objects = [
                obj for timestamp, obj in objects_dict.items()
                if current_date <= timestamp < next_date
            ]

            if filtered_objects:
                # Calculer la moyenne des valeurs
                avg_value = sum(float(obj.value) for obj in filtered_objects) / len(filtered_objects)

                # Ajouter le résultat à la liste de résultats
                result.append({
                    'recordedAt': current_date,
                    'value': avg_value
                })

            current_date = next_date
    
    '''
    aggregate by hour
    '''
    if aggregate_type == 2:
        # Convertir la liste d'objets en un dictionnaire avec recordedAt comme clé
        objects_dict = {obj.recordedAt: obj for obj in values}

        start_date = min(objects_dict.keys())
        end_date = max(objects_dict.keys())

        current_date = start_date
        while current_date <= end_date:
            next_date = current_date + timedelta(minutes=60)

            # Sélectionner les objets enregistrés entre current_date et next_date
            filtered_objects = [
                obj for timestamp, obj in objects_dict.items()
                if current_date <= timestamp < next_date
            ]

            if filtered_objects:
                # Calculer la moyenne des valeurs
                avg_value = sum(float(obj.value) for obj in filtered_objects) / len(filtered_objects)

                # Ajouter le résultat à la liste de résultats
                result.append({
                    'recordedAt': current_date,
                    'value': avg_value
                })

            current_date = next_date
    
    '''
    aggregate by day
    '''
    if aggregate_type == 3:
        # Convertir la liste d'objets en un dictionnaire avec recordedAt comme clé
        objects_dict = {obj.recordedAt: obj for obj in values}

        start_date = min(objects_dict.keys())
        end_date = max(objects_dict.keys())

        current_date = start_date
        while current_date <= end_date:
            next_date = current_date + timedelta(days=1)

            # Sélectionner les objets enregistrés entre current_date et next_date
            filtered_objects = [
                obj for timestamp, obj in objects_dict.items()
                if current_date <= timestamp < next_date
            ]

            if filtered_objects:
                # Calculer la moyenne des valeurs
                avg_value = sum(float(obj.value) for obj in filtered_objects) / len(filtered_objects)

                # Ajouter le résultat à la liste de résultats
                result.append({
                    'recordedAt': current_date,
                    'value': avg_value
                })

            current_date = next_date
    
    '''
    aggregate by week
    '''
    if aggregate_type == 4:
        # Convertir la liste d'objets en un dictionnaire avec recordedAt comme clé
        objects_dict = {obj.recordedAt: obj for obj in values}

        start_date = min(objects_dict.keys())
        end_date = max(objects_dict.keys())

        current_date = start_date
        while current_date <= end_date:
            next_date = current_date + timedelta(days=7)

            # Sélectionner les objets enregistrés entre current_date et next_date
            filtered_objects = [
                obj for timestamp, obj in objects_dict.items()
                if current_date <= timestamp < next_date
            ]

            if filtered_objects:
                # Calculer la moyenne des valeurs
                avg_value = sum(float(obj.value) for obj in filtered_objects) / len(filtered_objects)

                # Ajouter le résultat à la liste de résultats
                result.append({
                    'recordedAt': current_date,
                    'value': avg_value
                })

            current_date = next_date
    
    '''
    aggregate by month
    '''
    if aggregate_type == 5:
        # Convertir la liste d'objets en un dictionnaire avec recordedAt comme clé
        objects_dict = {obj.recordedAt: obj for obj in values}

        start_date = min(objects_dict.keys())
        end_date = max(objects_dict.keys())

        current_date = start_date
        while current_date <= end_date:
            next_date = current_date + timedelta(days=30)

            # Sélectionner les objets enregistrés entre current_date et next_date
            filtered_objects = [
                obj for timestamp, obj in objects_dict.items()
                if current_date <= timestamp < next_date
            ]

            if filtered_objects:
                # Calculer la moyenne des valeurs
                avg_value = sum(float(obj.value) for obj in filtered_objects) / len(filtered_objects)

                # Ajouter le résultat à la liste de résultats
                result.append({
                    'recordedAt': current_date,
                    'value': avg_value
                })

            current_date = next_date
            
    '''
    aggregate by year
    '''
    if aggregate_type == 6:
        # Convertir la liste d'objets en un dictionnaire avec recordedAt comme clé
        objects_dict = {obj.recordedAt: obj for obj in values}

        start_date = min(objects_dict.keys())
        end_date = max(objects_dict.keys())

        current_date = start_date
        while current_date <= end_date:
            next_date = current_date + timedelta(days=365)

            # Sélectionner les objets enregistrés entre current_date et next_date
            filtered_objects = [
                obj for timestamp, obj in objects_dict.items()
                if current_date <= timestamp < next_date
            ]

            if filtered_objects:
                # Calculer la moyenne des valeurs
                avg_value = sum(float(obj.value) for obj in filtered_objects) / len(filtered_objects)

                # Ajouter le résultat à la liste de résultats
                result.append({
                    'recordedAt': current_date,
                    'value': avg_value
                })

            current_date = next_date

    return result