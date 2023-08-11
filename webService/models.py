from django.db import models


method_choice = (
    (0, "Path"),
    (1, "GET")
)

content_type_choice = (
    (0, "JSON"),
    (1, "XML")
)

class WebService(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Web service name", max_length=100)
    method = models.IntegerField(verbose_name="Method to get data", choices=method_choice, default=0)
    contentType = models.IntegerField(verbose_name="Content of device response", choices=content_type_choice, default=0)
    active = models.BooleanField(default=True)
    path = models.CharField(verbose_name="Path of variable name response", max_length=80, null=True, blank=True)
    
    def __str__(self):
        return str(self.id) + " "+ self.name
    