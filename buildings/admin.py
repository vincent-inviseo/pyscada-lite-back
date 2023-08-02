from django.contrib import admin

from buildings.models import Building, Page, Device, Variable, AlertVariable, Chart, Unit, DeviceProtocol, Color, Scaling

admin.site.register(Building)
admin.site.register(Page)
admin.site.register(Device)
admin.site.register(Variable)
admin.site.register(AlertVariable)
admin.site.register(Chart)
admin.site.register(Unit)
admin.site.register(DeviceProtocol)
admin.site.register(Color)
admin.site.register(Scaling)