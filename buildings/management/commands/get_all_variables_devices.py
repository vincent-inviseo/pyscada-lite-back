from django.core.management.base import BaseCommand, CommandError
import requests
from buildings.models import Device
from buildings.serializers import VariableReadSerializer

from buildings.views import save_variable_value
from webService.models import WebService

class Command(BaseCommand):
    help = 'Contact all devices registred to get all values variables'

    def handle(self, *args, **options):
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