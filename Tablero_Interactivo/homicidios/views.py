# homicidios/views.py
from django.shortcuts import render
from .models import Homicidio

def mostrar_homicidios(request):
    homicidios = Homicidio.objects.all()
    return render(request, 'homicidios/mostrar_homicidios.html', {'homicidios': homicidios})
