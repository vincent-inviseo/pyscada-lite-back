# import datetime
# import json
# from os import getpid
# from sqlite3 import ProgrammingError
# from struct import pack, unpack
# import time
# from venv import logger
# from django.db import models
# from django.forms import ValidationError

# class DeviceProtocol(models.Model):
#     id = models.AutoField(primary_key=True)
#     protocol = models.CharField(max_length=400, default="generic")
#     description = models.TextField(default="", verbose_name="Description", null=True)
#     app_name = models.CharField(max_length=400, default="pyscada.PROTOCOL")
#     device_class = models.CharField(max_length=400, default="pyscada.PROTOCOL.device")
#     daq_daemon = models.BooleanField()
#     single_thread = models.BooleanField()

#     def __str__(self):
#         return self.protocol


# class Device(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=400, default="")
#     description = models.TextField(default="", verbose_name="Description", null=True)
#     active = models.BooleanField(default=True)
#     byte_order_choices = (
#         ("1-0-3-2", "1-0-3-2"),
#         ("0-1-2-3", "0-1-2-3"),
#         ("2-3-0-1", "2-3-0-1"),
#         ("3-2-1-0", "3-2-1-0"),
#     )
#     byte_order = models.CharField(
#         max_length=15, default="1-0-3-2", choices=byte_order_choices
#     )
#     polling_interval_choices = (
#         (0.1, "100 Milliseconds"),
#         (0.5, "500 Milliseconds"),
#         (1.0, "1 Second"),
#         (5.0, "5 Seconds"),
#         (10.0, "10 Seconds"),
#         (15.0, "15 Seconds"),
#         (30.0, "30 Seconds"),
#         (60.0, "1 Minute"),
#         (150.0, "2.5 Mintues"),
#         (300.0, "5 Minutes"),
#         (360.0, "6 Minutes (10 times per Hour)"),
#         (600.0, "10 Minutes"),
#         (900.0, "15 Minutes"),
#         (1800.0, "30 Minutes"),
#         (3600.0, "1 Hour"),
#         (21600.0, "6 Hours"),
#         (43200.0, "12 Hours"),
#         (86400.0, "1 Day"),
#         (604800.0, "1 Week"),
#     )
#     polling_interval = models.FloatField(
#         default=polling_interval_choices[3][0], choices=polling_interval_choices
#     )
#     protocol = models.ForeignKey(DeviceProtocol, null=True, on_delete=models.CASCADE)

#     def __str__(self):
#         # display protocol for the JS filter for inline variables (hmi.static.pyscada.js.admin)
#         if self.protocol is not None:
#             return self.protocol.protocol + "-" + self.name
#         else:
#             return "generic-" + self.short_name

#     def get_device_instance(self):
#         try:
#             mod = __import__(self.protocol.device_class, fromlist=["Device"])
#             device_class = getattr(mod, "Device")
#             return device_class(self)
#         except:
#             logger.error(
#                 f"{self.name}({getpid()}), unhandled exception", exc_info=True
#             )
#             return None

# class Unit(models.Model):
#     id = models.AutoField(primary_key=True)
#     unit = models.CharField(max_length=80, verbose_name="Unit")
#     description = models.TextField(default="", verbose_name="Description", null=True)
#     udunit = models.CharField(max_length=500, verbose_name="udUnit", default="")

#     def __str__(self):
#         return self.unit

#     class Meta:
#         managed = True
        

# class Scaling(models.Model):
#     id = models.AutoField(primary_key=True)
#     description = models.TextField(
#         default="", verbose_name="Description", null=True, blank=True
#     )
#     input_low = models.FloatField()
#     input_high = models.FloatField()
#     output_low = models.FloatField()
#     output_high = models.FloatField()
#     limit_input = models.BooleanField()

#     def __str__(self):
#         if self.description:
#             return self.description
#         else:
#             return (
#                 str(self.id)
#                 + "_["
#                 + str(self.input_low)
#                 + ":"
#                 + str(self.input_high)
#                 + "] -> ["
#                 + str(self.output_low)
#                 + ":"
#                 + str(self.output_low)
#                 + "]"
#             )

#     def scale_value(self, input_value):
#         input_value = float(input_value)
#         if self.limit_input:
#             input_value = max(min(input_value, self.input_high), self.input_low)
#         norm_value = (input_value - self.input_low) / (self.input_high - self.input_low)
#         return norm_value * (self.output_high - self.output_low) + self.output_low

#     def scale_output_value(self, input_value):
#         input_value = float(input_value)
#         norm_value = (input_value - self.output_low) / (
#             self.output_high - self.output_low
#         )
#         return norm_value * (self.input_high - self.input_low) + self.input_low

# class Color(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.SlugField(max_length=80, verbose_name="variable name")
#     R = models.PositiveSmallIntegerField(default=0)
#     G = models.PositiveSmallIntegerField(default=0)
#     B = models.PositiveSmallIntegerField(default=0)

#     def __str__(self):
#         return (
#             "rgb(" + str(self.R) + ", " + str(self.G) + ", " + str(self.B) + ", " + ")"
#         )

#     def color_code(self):
#         return "#%02x%02x%02x" % (self.R, self.G, self.B)

#     def color_rect_html(self):
#         return (
#             '<div style="width:4px;height:0;border:5px solid #%02x%02x%02x;overflow:hidden"></div>'
#             % (self.R, self.G, self.B)
#         )


# class Variable(models.Model):
#     """
#     Stores a variable entry, related to :mod:`pyscada.Device`,
#     :mod:`pyscada.Unit`, (optional) :mod:`pyscada.Scaling`,
#     (optional) :mod:`pyscada.Color` and (optional) :mod:`pyscada.Dictionary`.
#     """

#     id = models.AutoField(primary_key=True)
#     name = models.SlugField(max_length=200, verbose_name="variable name", unique=True)
#     description = models.TextField(default="", verbose_name="Description")
#     device = models.ForeignKey(Device, null=True, on_delete=models.CASCADE)
#     active = models.BooleanField(default=True)
#     unit = models.ForeignKey(Unit, on_delete=models.SET(1))
#     writeable = models.BooleanField(default=False)
#     value_class_choices = (
#         ("FLOAT32", "REAL (FLOAT32)"),
#         ("FLOAT32", "SINGLE (FLOAT32)"),
#         ("FLOAT32", "FLOAT32"),
#         ("UNIXTIMEF32", "UNIXTIMEF32"),
#         ("FLOAT64", "LREAL (FLOAT64)"),
#         ("FLOAT64", "FLOAT  (FLOAT64)"),
#         ("FLOAT64", "DOUBLE (FLOAT64)"),
#         ("FLOAT64", "FLOAT64"),
#         ("UNIXTIMEF64", "UNIXTIMEF64"),
#         ("FLOAT48", "FLOAT48"),
#         ("INT64", "INT64"),
#         ("UINT64", "UINT64"),
#         ("UNIXTIMEI64", "UNIXTIMEI64"),
#         ("INT48", "INT48"),
#         ("UNIXTIMEI32", "UNIXTIMEI32"),
#         ("INT32", "INT32"),
#         ("UINT32", "DWORD (UINT32)"),
#         ("UINT32", "UINT32"),
#         ("INT16", "INT (INT16)"),
#         ("INT16", "INT16"),
#         ("UINT16", "WORD (UINT16)"),
#         ("UINT16", "UINT (UINT16)"),
#         ("UINT16", "UINT16"),
#         ("INT8", "INT8"),
#         ("UINT8", "UINT8"),
#         ("BOOLEAN", "BOOL (BOOLEAN)"),
#         ("BOOLEAN", "BOOLEAN"),
#     )
#     scaling = models.ForeignKey(
#         Scaling, null=True, blank=True, on_delete=models.SET_NULL
#     )
#     value_class = models.CharField(
#         max_length=15,
#         default="FLOAT64",
#         verbose_name="value_class",
#         choices=value_class_choices,
#     )
#     cov_increment = models.FloatField(default=0, verbose_name="COV")
#     byte_order_choices = (
#         (
#             "default",
#             "default (specified by device byte order)",
#         ),
#         ("1-0-3-2", "1-0-3-2"),
#         ("0-1-2-3", "0-1-2-3"),
#         ("2-3-0-1", "2-3-0-1"),
#         ("3-2-1-0", "3-2-1-0"),
#     )
#     short_name = models.CharField(
#         default="", max_length=80, verbose_name="variable short name", blank=True
#     )
#     chart_line_color = models.ForeignKey(
#         Color, null=True, default=None, blank=True, on_delete=models.SET_NULL
#     )
#     chart_line_thickness_choices = ((3, "3Px"),)
#     chart_line_thickness = models.PositiveSmallIntegerField(
#         default=3, choices=chart_line_thickness_choices
#     )
#     value_min = models.FloatField(null=True, blank=True)
#     value_max = models.FloatField(null=True, blank=True)
#     min_type_choices = (
#         ("lte", "<="),
#         ("lt", "<"),
#     )
#     max_type_choices = (
#         ("gte", ">="),
#         ("gt", ">"),
#     )
#     min_type = models.CharField(max_length=4, default="lte", choices=min_type_choices)
#     max_type = models.CharField(max_length=4, default="gte", choices=max_type_choices)

#     def hmi_name(self):
#         if self.short_name and self.short_name != "-" and self.short_name != "":
#             return self.short_name
#         else:
#             return self.name

#     def chart_line_color_code(self):
#         if self.chart_line_color and self.chart_line_color.id != 1:
#             return self.chart_line_color.color_code()
#         else:
#             c = 51
#             c_id = self.pk + 1
#             c = c % c_id
#             while c >= 51:
#                 c_id = c_id - c
#                 c = c % c_id
#             return Color.objects.get(id=c_id).color_code()

#     """
#     M: Mantissa
#     E: Exponent
#     S: Sign
#     uint 0            uint 1
#     byte 0   byte 1   byte 2   byte 3
#     1-0-3-2 MMMMMMMM MMMMMMMM SEEEEEEE EMMMMMMM
#     0-1-2-3 MMMMMMMM MMMMMMMM EMMMMMMM SEEEEEEE
#     2-3-0-1 EMMMMMMM SEEEEEEE MMMMMMMM MMMMMMMM
#     3-2-1-0 SEEEEEEE EMMMMMMM MMMMMMMM MMMMMMMM
#     """

#     byte_order = models.CharField(
#         max_length=15, default="default", choices=byte_order_choices
#     )

#     # for RecodedVariable
#     value = None
#     prev_value = None
#     store_value = False
#     timestamp_old = None
#     timestamp = None

#     def __str__(self):
#         return str(self.id) + " - " + self.name

#     def add_attr(self, **kwargs):
#         for key in kwargs:
#             setattr(self, key, kwargs[key])

#     def item_type(self):
#         return "variable"

#     def get_bits_by_class(self):
#         """
#         `BOOLEAN`							1	1/16 WORD
#         `UINT8` `BYTE`						8	1/2 WORD
#         `INT8`								8	1/2 WORD
#         `UNT16` `WORD`						16	1 WORD
#         `INT16`	`INT`						16	1 WORD
#         `UINT32` `DWORD`					32	2 WORD
#         `INT32`								32	2 WORD
#         `FLOAT32` `REAL` `SINGLE` 			32	2 WORD
#         `FLOAT48` 'INT48'                  	48	3 WORD
#         `FLOAT64` `LREAL` `FLOAT` `DOUBLE`	64	4 WORD
#         """
#         if self.value_class.upper() in [
#             "FLOAT64",
#             "DOUBLE",
#             "FLOAT",
#             "LREAL",
#             "UNIXTIMEI64",
#             "UNIXTIMEF64",
#             "INT64",
#             "UINT64",
#         ]:
#             return 64
#         if self.value_class.upper() in ["FLOAT48", "INT48"]:
#             return 48
#         if self.value_class.upper() in [
#             "FLOAT32",
#             "SINGLE",
#             "INT32",
#             "UINT32",
#             "DWORD",
#             "BCD32",
#             "BCD24",
#             "REAL",
#             "UNIXTIMEI32",
#             "UNIXTIMEF32",
#         ]:
#             return 32
#         if self.value_class.upper() in [
#             "INT16",
#             "INT",
#             "WORD",
#             "UINT",
#             "UINT16",
#             "BCD16",
#         ]:
#             return 16
#         if self.value_class.upper() in ["INT8", "UINT8", "BYTE", "BCD8"]:
#             return 8
#         if self.value_class.upper() in ["BOOL", "BOOLEAN"]:
#             return 1
#         else:
#             return 16

#     def query_prev_value(self, time_min=None, use_protocol_variable=True):
#         """
#         get the last value and timestamp from the database
#         """
#         pv = self.get_protocol_variable()
#         if use_protocol_variable and pv is not None and hasattr(pv, "query_prev_value"):
#             return pv.query_prev_value(time_min)

#         time_max = time.time() * 2097152 * 1000 + 2097151
#         if time_min is None:
#             time_min = time_max - (3 * 3660 * 1000 * 2097152)
#         val = self.recordeddata_set.filter(id__range=(time_min, time_max)).last()
#         if val:
#             self.prev_value = val.value()
#             self.timestamp_old = val.timestamp
#             return True
#         else:
#             return False

#     def update_value(self, value=None, timestamp=None):
#         """
#         update the value in the instance and detect value state change
#         """

#         try:
#             value = float(value)
#         except ValueError:
#             # Add string value in dictionary and replace the string by the dictionary value
#             if type(value) == str:
#                 value = self.convert_string_value(value)
#             else:
#                 logger.info(
#                     "Value read for %s format not supported : %s" % (self, type(value))
#                 )
#                 value = None
#         except TypeError:
#             pass

#         if (
#             self.scaling is None
#             or value is None
#             or self.value_class.upper() in ["BOOL", "BOOLEAN"]
#         ):
#             self.value = value
#         else:
#             self.value = self.scaling.scale_value(value)
#         self.timestamp = timestamp
#         self.store_value = False
#         if self.prev_value is None:
#             # no prev value in the cache, always store the value
#             self.store_value = True
#             self.timestamp_old = self.timestamp
#         elif self.value is None:
#             # value could not be queried
#             self.store_value = False
#         elif abs(self.prev_value - self.value) <= self.cov_increment:
#             if self.timestamp_old is None:
#                 self.store_value = True
#                 self.timestamp_old = self.timestamp
#             else:
#                 if (self.timestamp - self.timestamp_old) >= 3600:
#                     # store at least every hour one value
#                     # store Value if old Value is older than 1 hour
#                     self.store_value = True
#                     self.timestamp_old = self.timestamp

#         else:
#             # value has changed
#             self.store_value = True
#             self.timestamp_old = self.timestamp
#         self.prev_value = self.value
#         return self.store_value

#     def decode_value(self, value):
#         #
#         if self.byte_order == "default":
#             byte_order = self.device.byte_order
#         else:
#             byte_order = self.byte_order

#         if self.value_class.upper() in ["FLOAT32", "SINGLE", "REAL", "UNIXTIMEF32"]:
#             target_format = "f"
#             source_format = "2H"
#         elif self.value_class.upper() in ["UINT32", "DWORD", "UNIXTIMEI32"]:
#             target_format = "I"
#             source_format = "2H"
#         elif self.value_class.upper() in ["INT32"]:
#             target_format = "i"
#             source_format = "2H"
#         elif self.value_class.upper() in ["FLOAT48"]:
#             target_format = "f"
#             source_format = "3H"
#         elif self.value_class.upper() in ["INT48"]:
#             target_format = "q"
#             source_format = "3H"
#         elif self.value_class.upper() in [
#             "FLOAT64",
#             "DOUBLE",
#             "FLOAT",
#             "LREAL",
#             "UNIXTIMEF64",
#         ]:
#             target_format = "d"
#             source_format = "4H"
#         elif self.value_class.upper() in ["UINT64"]:
#             target_format = "Q"
#             source_format = "4H"
#         elif self.value_class.upper() in ["INT64", "UNIXTIMEI64"]:
#             target_format = "q"
#             source_format = "4H"
#         elif self.value_class.upper() in ["INT16", "INT"]:
#             if byte_order in ["1-0-3-2", "3-2-1-0"]:
#                 # only convert to from uint to int
#                 return unpack("h", pack("H", value[0]))[0]
#             else:
#                 # swap bytes
#                 return unpack(">h", pack("<H", value[0]))[0]
#         elif self.value_class.upper() in ["BCD32", "BCD24", "BCD16"]:
#             target_format = "f"
#             source_format = "2H"
#             return value[0]
#         else:
#             return value[0]

#         #
#         if source_format == "2H":
#             if byte_order == "1-0-3-2":
#                 return unpack(target_format, pack(source_format, value[0], value[1]))[0]
#             if byte_order == "3-2-1-0":
#                 return unpack(target_format, pack(source_format, value[1], value[0]))[0]
#             if byte_order == "0-1-2-3":
#                 return unpack(
#                     target_format,
#                     pack(
#                         source_format,
#                         unpack(">H", pack("<H", value[0]))[0],
#                         unpack(">H", pack("<H", value[1]))[0],
#                     ),
#                 )[0]
#             if byte_order == "2-3-0-1":
#                 return unpack(
#                     target_format,
#                     pack(
#                         source_format,
#                         unpack(">H", pack("<H", value[1]))[0],
#                         unpack(">H", pack("<H", value[0]))[0],
#                     ),
#                 )[0]
#         elif source_format == "3H":
#             source_format = "4H"
#             if byte_order == "1-0-3-2":
#                 return unpack(
#                     target_format, pack(source_format, 0, value[0], value[1], value[2])
#                 )[0]
#             if byte_order == "3-2-1-0":
#                 return unpack(
#                     target_format, pack(source_format, value[2], value[1], value[0], 0)
#                 )[0]
#             if byte_order == "0-1-2-3":
#                 return unpack(
#                     target_format,
#                     pack(
#                         source_format,
#                         0,
#                         unpack(">H", pack("<H", value[0]))[0],
#                         unpack(">H", pack("<H", value[1]))[0],
#                         unpack(">H", pack("<H", value[2]))[0],
#                     ),
#                 )[0]
#             if byte_order == "2-3-0-1":
#                 return unpack(
#                     target_format,
#                     pack(
#                         source_format,
#                         0,
#                         unpack(">H", pack("<H", value[2]))[0],
#                         unpack(">H", pack("<H", value[1]))[0],
#                         unpack(">H", pack("<H", value[0]))[0],
#                     ),
#                 )[0]
#             source_format = "3H"
#         else:
#             if byte_order == "1-0-3-2":
#                 return unpack(
#                     target_format,
#                     pack(source_format, value[0], value[1], value[2], value[3]),
#                 )[0]
#             if byte_order == "3-2-1-0":
#                 return unpack(
#                     target_format,
#                     pack(source_format, value[3], value[2], value[1], value[0]),
#                 )[0]
#             if byte_order == "0-1-2-3":
#                 return unpack(
#                     target_format,
#                     pack(
#                         source_format,
#                         unpack(">H", pack("<H", value[0])),
#                         unpack(">H", pack("<H", value[1])),
#                         unpack(">H", pack("<H", value[2])),
#                         unpack(">H", pack("<H", value[3])),
#                     ),
#                 )[0]
#             if byte_order == "2-3-0-1":
#                 return unpack(
#                     target_format,
#                     pack(
#                         source_format,
#                         unpack(">H", pack("<H", value[3])),
#                         unpack(">H", pack("<H", value[2])),
#                         unpack(">H", pack("<H", value[1])),
#                         unpack(">H", pack("<H", value[0])),
#                     ),
#                 )[0]

#     def encode_value(self, value):
#         if self.value_class.upper() in ["FLOAT32", "SINGLE", "REAL", "UNIXTIMEF32"]:
#             source_format = "f"
#             target_format = "2H"
#         elif self.value_class.upper() in ["UINT32", "DWORD", "UNIXTIMEI32"]:
#             source_format = "I"
#             target_format = "2H"
#         elif self.value_class.upper() in ["INT32"]:
#             source_format = "i"
#             target_format = "2H"
#         elif self.value_class.upper() in ["FLOAT48"]:
#             source_format = "f"
#             target_format = "3H"
#         elif self.value_class.upper() in ["INT48"]:
#             source_format = "q"
#             target_format = "3H"
#         elif self.value_class.upper() in [
#             "FLOAT64",
#             "DOUBLE",
#             "FLOAT",
#             "LREAL",
#             "UNIXTIMEF64",
#         ]:
#             source_format = "d"
#             target_format = "4H"
#         elif self.value_class.upper() in ["UINT64"]:
#             source_format = "Q"
#             target_format = "4H"
#         elif self.value_class.upper() in ["INT64", "UNIXTIMEI64"]:
#             source_format = "q"
#             target_format = "4H"

#         elif self.value_class.upper() in ["BCD32", "BCD24", "BCD16"]:
#             source_format = "f"
#             target_format = "2H"
#             return value[0]
#         else:
#             return value[0]
#         output = unpack(target_format, pack(source_format, value))
#         #
#         if self.byte_order == "default":
#             byte_order = self.device.byte_order
#         else:
#             byte_order = self.byte_order
#         if target_format == "2H":
#             if byte_order == "1-0-3-2":
#                 return output
#             if byte_order == "3-2-1-0":
#                 return [output[1], output[0]]
#             if byte_order == "0-1-2-3":
#                 return [
#                     unpack(">H", pack("<H", output[0])),
#                     unpack(">H", pack("<H", output[1])),
#                 ]
#             if byte_order == "2-3-0-1":
#                 return [
#                     unpack(">H", pack("<H", output[1])),
#                     unpack(">H", pack("<H", output[0])),
#                 ]
#         elif target_format == "3H":
#             if byte_order == "1-0-3-2":
#                 return output
#             if byte_order == "3-2-1-0":
#                 return [output[2], output[1], output[0]]
#             if byte_order == "0-1-2-3":
#                 return [
#                     unpack(">H", pack("<H", output[0]))[0],
#                     unpack(">H", pack("<H", output[1]))[0],
#                     unpack(">H", pack("<H", output[2]))[0],
#                 ]
#             if byte_order == "2-3-0-1":
#                 return [
#                     unpack(">H", pack("<H", output[2]))[0],
#                     unpack(">H", pack("<H", output[1]))[0],
#                     unpack(">H", pack("<H", output[0]))[0],
#                 ]
#         else:
#             if byte_order == "1-0-3-2":
#                 return output
#             if byte_order == "3-2-1-0":
#                 return [output[3], output[2], output[1], output[0]]
#             if byte_order == "0-1-2-3":
#                 return [
#                     unpack(">H", pack("<H", output[0])),
#                     unpack(">H", pack("<H", output[1])),
#                     unpack(">H", pack("<H", output[2])),
#                     unpack(">H", pack("<H", output[3])),
#                 ]
#             if byte_order == "2-3-0-1":
#                 return [
#                     unpack(">H", pack("<H", output[3])),
#                     unpack(">H", pack("<H", output[2])),
#                     unpack(">H", pack("<H", output[1])),
#                     unpack(">H", pack("<H", output[0])),
#                 ]
                

#     def get_protocol_variable(self):
#         related_variables = [
#             field
#             for field in Variable._meta.get_fields()
#             if issubclass(type(field), OneToOneRel)
#         ]
#         for v in related_variables:
#             try:
#                 if (
#                     hasattr(self, v.name)
#                     and hasattr(getattr(self, v.name), "protocol_id")
#                     and hasattr(self, "device")
#                     and getattr(self, v.name).protocol_id == self.device.protocol.id
#                 ):
#                     return getattr(self, v.name)
#             except ProgrammingError:
#                 pass
#         return None


# def validate_nonzero(value):
#     if value == 0:
#         raise ValidationError(
#             _("Quantity %(value)s is not allowed"),
#             params={"value": value},
#         )


# def start_from_default():
#     return datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
    
# class Dictionary(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=400, default="")

#     def __str__(self):
#         return str(self.id) + ": " + self.name

#     def append(self, label, value, silent=False, update=None):
#         if update is None:
#             _, created = DictionaryItem.objects.get_or_create(
#                 label=label, value=value, dictionary=self
#             )
#             if not created and not silent:
#                 logger.warning(
#                     "Item ({}:{}) for dictionary {} already exist".format(
#                         label, value, self
#                     )
#                 )
#         elif update == "label":
#             DictionaryItem.objects.update_or_create(
#                 value=value,
#                 dictionary=self,
#                 defaults={
#                     "label": label,
#                 },
#             )
#         elif update == "value":
#             DictionaryItem.objects.update_or_create(
#                 label=label,
#                 dictionary=self,
#                 defaults={
#                     "value": value,
#                 },
#             )

#     def remove(self, label=None, value=None):
#         if label is not None and value is not None:
#             DictionaryItem.objects.filter(label=label, value=value).delete()
#         elif label is not None:
#             DictionaryItem.objects.filter(label=label).delete()
#         elif value is not None:
#             DictionaryItem.objects.filter(value=value).delete()


# class DictionaryItem(models.Model):
#     id = models.AutoField(primary_key=True)
#     label = models.CharField(max_length=400, default="", blank=True)
#     value = models.CharField(max_length=400, default="")
#     dictionary = models.ForeignKey(
#         Dictionary, blank=True, null=True, on_delete=models.CASCADE
#     )

#     def __str__(self):
#         return str(self.id) + ": " + self.label

