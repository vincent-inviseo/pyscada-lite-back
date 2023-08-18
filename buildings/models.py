from django.db import models
from django.utils.translation import gettext_lazy as _
from os import getpid
from venv import logger
from django.db import models

from config import settings
from webService.models import WebService

'''
CHOICES
'''

MIN_TYPE_CHOICE = (
    ("lte", "<="),
    ("lt", "<"),
)

MAX_TYPE_CHOICE = (
    ("gte", ">="),
    ("gt", ">"),
)

VALUE_CLASS_CHOICE = (
        ("FLOAT32", "REAL (FLOAT32)"),
        ("FLOAT32", "SINGLE (FLOAT32)"),
        ("FLOAT32", "FLOAT32"),
        ("UNIXTIMEF32", "UNIXTIMEF32"),
        ("FLOAT64", "LREAL (FLOAT64)"),
        ("FLOAT64", "FLOAT  (FLOAT64)"),
        ("FLOAT64", "DOUBLE (FLOAT64)"),
        ("FLOAT64", "FLOAT64"),
        ("UNIXTIMEF64", "UNIXTIMEF64"),
        ("FLOAT48", "FLOAT48"),
        ("INT64", "INT64"),
        ("UINT64", "UINT64"),
        ("UNIXTIMEI64", "UNIXTIMEI64"),
        ("INT48", "INT48"),
        ("UNIXTIMEI32", "UNIXTIMEI32"),
        ("INT32", "INT32"),
        ("UINT32", "DWORD (UINT32)"),
        ("UINT32", "UINT32"),
        ("INT16", "INT (INT16)"),
        ("INT16", "INT16"),
        ("UINT16", "WORD (UINT16)"),
        ("UINT16", "UINT (UINT16)"),
        ("UINT16", "UINT16"),
        ("INT8", "INT8"),
        ("UINT8", "UINT8"),
        ("BOOLEAN", "BOOL (BOOLEAN)"),
        ("BOOLEAN", "BOOLEAN"),
    )

BYTE_ORDER = (
    ("1-0-3-2", "1-0-3-2"),
    ("0-1-2-3", "0-1-2-3"),
    ("2-3-0-1", "2-3-0-1"),
    ("3-2-1-0", "3-2-1-0"),
)

CHART_LINE_TRICKNESS = (
    (3, "3Px"),
)

WIDTH_CHOICES = (
    ("25%", "25%"),
    ("33%", "33%"),
    ("50%", "50%"),
    ("75%", "75%"),
    ("100%", "100%")
)

PROTOCOLE_CHOICE = (
    ("Web Service", "Web Service"),
    ("Modbus", "Modbus"),
    ("BacNet", "BacNet")
)

CHARTS_TYPE = (
    (0, 'BARS'),
    (1, 'LINES'),
    (2, 'DONUT'),
    (3, 'GAUGE'),
    (4, 'LOAD PROFIL')
)

POOLING_INTERVALE = (
        (0.1, "100 Milliseconds"),
        (0.5, "500 Milliseconds"),
        (1.0, "1 Second"),
        (5.0, "5 Seconds"),
        (10.0, "10 Seconds"),
        (15.0, "15 Seconds"),
        (30.0, "30 Seconds"),
        (60.0, "1 Minute"),
        (150.0, "2.5 Mintues"),
        (300.0, "5 Minutes"),
        (360.0, "6 Minutes (10 times per Hour)"),
        (600.0, "10 Minutes"),
        (900.0, "15 Minutes"),
        (1800.0, "30 Minutes"),
        (3600.0, "1 Hour"),
        (21600.0, "6 Hours"),
        (43200.0, "12 Hours"),
        (86400.0, "1 Day"),
        (604800.0, "1 Week"),
    )

class Building(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='buildings',
        null=True,
        on_delete=models.SET_NULL,
        )
    name = models.CharField("Building name", max_length=100)
    address = models.CharField("Building address", max_length=200)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    position = models.IntegerField("Position in the list")
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name
    
class Page(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Page name", max_length=100)
    link_name = models.CharField("Link name", max_length=50)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    position = models.IntegerField("Position in the list")
    visible = models.BooleanField(default=True)
    building = models.ForeignKey(
        'Building', null=True, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

    
class Chart(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Chart name", max_length=100)
    legende_axe_x = models.CharField("Legende X", default="axe X", max_length=100, blank=True)
    legende_axe_y = models.CharField("Legende X", default="axe Y", max_length=100, blank=True)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField(blank=True)
    width =   models.CharField(choices=WIDTH_CHOICES, default="100%", max_length=10, blank=True)
    position = models.IntegerField("Position in the list")
    visible = models.BooleanField(default=True)
    variables = models.ManyToManyField('Variable')
    chartType = models.IntegerField(verbose_name="Chart Type", choices=CHARTS_TYPE, null=True, default=0)
    pages = models.ManyToManyField('Page')
    
    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name
    
class Device(models.Model):
    id = models.AutoField(primary_key=True)
    short_name = models.CharField("Device name", max_length=70)
    description = models.CharField("Device description", max_length=300, null=True, blank=True)
    variables = models.ManyToManyField('Variable', blank=True)
    active = models.BooleanField(default=True)
    byte_order = models.CharField(
         max_length=15, default="1-0-3-2", choices=BYTE_ORDER
    )
    polling_interval = models.FloatField(
        default=POOLING_INTERVALE[3][0], choices=POOLING_INTERVALE
    )  
    address = models.CharField(verbose_name="Address of this device", max_length=200, null=True) 
    protocol = models.ForeignKey('DeviceProtocol', null=True, on_delete=models.DO_NOTHING, blank=True)

    def __str__(self):
        # display protocol for the JS filter for inline variables (hmi.static.pyscada.js.admin)
        if self.protocol is not None:
            return self.protocol.protocol + "-" + self.short_name
        else:
            return "generic-" + self.short_name

    def get_device_instance(self):
        try:
            mod = __import__(self.protocol.device_class, fromlist=["Device"])
            device_class = getattr(mod, "Device")
            return device_class(self)
        except:
            logger.error(
                f"{self.short_name}({getpid()}), unhandled exception", exc_info=True
            )
            return None

class DeviceProtocol(models.Model):
    id = models.AutoField(primary_key=True)
    protocol = models.CharField(max_length=20, verbose_name="Protocol", choices=PROTOCOLE_CHOICE)
    description = models.TextField(default="", verbose_name="Description", null=True, blank=True)

    def __str__(self):
        return self.protocol


class Variable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.SlugField(max_length=200, verbose_name="variable name", unique=True)
    description = models.TextField(default="", verbose_name="Description", null=True, blank=True)
    active = models.BooleanField(default=True)
    unit = models.ForeignKey('Unit', on_delete=models.SET(1))
    alerts = models.ForeignKey('AlertVariable', on_delete=models.CASCADE, blank=True, null=True)
    writeable = models.BooleanField(default=False)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField(blank=True)
    webService = models.ForeignKey(WebService, on_delete=models.CASCADE, null=True)
    scaling = models.ForeignKey(
        'Scaling', null=True, blank=True, on_delete=models.SET_NULL
    )
    value_class = models.CharField(
        max_length=15,
        default="FLOAT64",
        verbose_name="value_class",
        choices=VALUE_CLASS_CHOICE,
    )
    cov_increment = models.FloatField(default=0, verbose_name="COV")
    chart_line_color = models.ForeignKey(
        'Color', null=True, default=None, blank=True, on_delete=models.SET_NULL
    )
    chart_line_thickness = models.PositiveSmallIntegerField(
        default=3, choices=CHART_LINE_TRICKNESS
    )
    value_min = models.FloatField(null=True, blank=True)
    value_max = models.FloatField(null=True, blank=True)
    min_type = models.CharField(max_length=4, default="lte", choices=MIN_TYPE_CHOICE)
    max_type = models.CharField(max_length=4, default="gte", choices=MAX_TYPE_CHOICE)

    def hmi_name(self):
        if self.short_name and self.short_name != "-" and self.short_name != "":
            return self.short_name
        else:
            return self.name

    def chart_line_color_code(self):
        if self.chart_line_color and self.chart_line_color.id != 1:
            return self.chart_line_color.color_code()
        else:
            c = 51
            c_id = self.pk + 1
            c = c % c_id
            while c >= 51:
                c_id = c_id - c
                c = c % c_id
            return Color.objects.get(id=c_id).color_code()
    
    def __str__(self):
        return self.name


class VariableValues(models.Model):
    id = models.AutoField(primary_key=True)
    recordedAt = models.DateTimeField(editable=False, auto_now_add=True)
    value = models.CharField(editable=False, max_length=200, null=True, blank=True)
    variable = models.ForeignKey(
        'Variable', null=True, on_delete=models.CASCADE
    )    


class Unit(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.CharField(max_length=80, verbose_name="Unit")
    description = models.TextField(default="", verbose_name="Description", null=True)
    udunit = models.CharField(max_length=500, verbose_name="udUnit", default="")

    def __str__(self):
        return self.unit

    class Meta:
        managed = True

class Color(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.SlugField(max_length=80, verbose_name="variable name")
    R = models.PositiveSmallIntegerField(default=0)
    G = models.PositiveSmallIntegerField(default=0)
    B = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return (
            "rgb(" + str(self.R) + ", " + str(self.G) + ", " + str(self.B) + ", " + ")"
        )

    def color_code(self):
        return "#%02x%02x%02x" % (self.R, self.G, self.B)
    
class Scaling(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(
        default="", verbose_name="Description", null=True, blank=True
    )
    input_low = models.FloatField()
    input_high = models.FloatField()
    output_low = models.FloatField()
    output_high = models.FloatField()
    limit_input = models.BooleanField()

    def __str__(self):
        if self.description:
            return self.description
        else:
            return (
                str(self.id)
                + "_["
                + str(self.input_low)
                + ":"
                + str(self.input_high)
                + "] -> ["
                + str(self.output_low)
                + ":"
                + str(self.output_low)
                + "]"
            )

    def scale_value(self, input_value):
        input_value = float(input_value)
        if self.limit_input:
            input_value = max(min(input_value, self.input_high), self.input_low)
        norm_value = (input_value - self.input_low) / (self.input_high - self.input_low)
        return norm_value * (self.output_high - self.output_low) + self.output_low

    def scale_output_value(self, input_value):
        input_value = float(input_value)
        norm_value = (input_value - self.output_low) / (
            self.output_high - self.output_low
        )
        return norm_value * (self.input_high - self.input_low) + self.input_low


class AlertVariable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Alert Variable Name", max_length=100)
    description = models.CharField("Description of alert", max_length=200, null=True, blank=True)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField(blank=True)
    
    class Meta:
        ordering = ['-createdAt']