# models.py
from django.db import models

class Entidad(models.Model):
    nombre = models.CharField(max_length=100)

class Municipio(models.Model):
    nombre = models.CharField(max_length=100)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)

class Fuente(models.Model):
    nombre = models.CharField(max_length=100)

class Homicidio(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    fecha = models.DateField()
    total = models.IntegerField()  # Campo para almacenar el total de homicidios
    fuente = models.ForeignKey(Fuente, on_delete=models.CASCADE, null=True, blank=True)


class EstadisticaDiaria(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    fecha = models.DateField()
    total_homicidios = models.IntegerField()
