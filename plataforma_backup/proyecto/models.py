from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Marca(models.Model):
    name_marca = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name_marca}"

class backup(models.Model):
    name_backup = models.CharField(max_length=250)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name_backup}"

class Equipo(models.Model):
    name_equipo = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipos')
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='marcas')

    def __str__(self):
        return f"{self.name_equipo} ({self.ip})"

opciones_status = [
    [0, "Respaldado"],
    [1, "No respaldado"],
]

class detalle_backup(models.Model):
    status = models.IntegerField(choices=opciones_status)
    registro = models.TextField(blank=True)
    contenido = models.FileField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    id_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name="detalles")
    id_backup = models.ForeignKey(backup, on_delete=models.CASCADE, related_name="backup", null = True, blank=True)

    def __str__(self):
        return f"{self.contenido}, {self.status}"

class TareaProgramada(models.Model):
    minutos = models.CharField(max_length=50)
    hora = models.CharField(max_length=50)
    dia = models.CharField(max_length=50)
    mes = models.CharField(max_length=50)
    dia_semana = models.CharField(max_length=50)

    def __str__(self):
        return f"Tarea programada {self.id}"