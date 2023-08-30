from django.db import models
from buildings.models import Device

'''
Modbus protocol method choice
'''
mode_protocol_choice = (
    ("rtu", "RTU"),
    ('tcp', "TCP/IP"),
)

parity_choice = (
    ("N", "None"),
    ("E", "Even"),
    ("O", "Odd")
)

stopbites_choice = (
    (1, "1"),
    (2, "2"),
)

bytesize_choice = (
    (8, "8"),
    (7, "7"),
)

class ModBusService(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="modbus service name", max_length=100)
    method = models.IntegerField(verbose_name="Mode du protocole", choices=mode_protocol_choice)
    rtu_slave_addesse = models.IntegerField(verbose_name="Adresse de l'eclave en mode RTU", blank=True)
    port_or_address = models.CharField(verbose_name="Adresse du peripherique (TCP/IP) ou port (RTU)", max_length=50)
    active = models.BooleanField(default=True)
    baudrate = models.IntegerField(verbose_name="Vitesse en baude", default=9600)
    stopbits = models.IntegerField(verbose_name="Nombre de bits de stop", default=1, choices=stopbites_choice)
    bytesize = models.IntegerField(verbose_name="Vitesse en baude", default=8, choices=bytesize_choice)
    starting_address: models.CharField(verbose_name="Adresse de depart du registre à lire", max_length=10)
    number_register_to_read = models.IntegerField(verbose_name="Nombre de registre à lire")
    timeout = models.IntegerField(verbose_name="Configuration du timeout en seconde", default=1)
    device = models.ForeignKey(Device, verbose_name="Peripherique associé au service", on_delete=models.CASCADE)
    server_port = models.IntegerField(verbose_name="Port du serveur dans le cas du TCP/IP", blank=True)
    
    def __str__(self):
        return self.name