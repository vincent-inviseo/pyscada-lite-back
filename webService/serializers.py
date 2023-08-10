from webService.models import WebService
from rest_framework import serializers


class WebServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebService
        fields = "__all__"