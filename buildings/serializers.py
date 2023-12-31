from rest_framework import serializers

from .models import Building, Page, Chart, Device, Unit, Variable, AlertVariable, VariableValues

class BuildingReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__"

class UnitReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"

class PageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"

class ChartReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = "__all__"
        
class DeviceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"

class VariableReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = "__all__"
        
class VariableValueReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariableValues
        fields = "__all__"

class AlertVariableReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertVariable
        fields = "__all__"