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
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    fecha = models.DateField()
    hombres = models.IntegerField()
    mujeres = models.IntegerField()
    no_identificado = models.IntegerField()
    fuente = models.ForeignKey(Fuente, on_delete=models.CASCADE)

class EstadisticaDiaria(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    fecha = models.DateField()
    total_homicidios = models.IntegerField()
