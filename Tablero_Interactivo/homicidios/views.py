import json
from django.shortcuts import render
from django.conf import settings
import os
from django.db.models import Sum
import plotly.graph_objects as go
from .models import EstadisticaDiaria, Entidad
from plotly.utils import PlotlyJSONEncoder  # Importación correcta
from .models import Homicidio, Entidad

def dashboard(request):
    # Obtener el año seleccionado del parámetro de consulta
    year = request.GET.get('year', None)

    # Lista de nombres de estados válidos
    estados_validos = [
        "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua",
        "Ciudad de México", "Coahuila", "Colima", "Durango", "Estado de México", "Guanajuato", "Guerrero",
        "Hidalgo", "Jalisco", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla",
        "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas",
        "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
    ]

    # Filtrar homicidios por año si está seleccionado
    homicidios_data = Homicidio.objects.filter(entidad__nombre__in=estados_validos)
    if year:
        homicidios_data = homicidios_data.filter(fecha__year=year)

    homicidios_data = homicidios_data.values('entidad__nombre').annotate(total_homicidios=Sum('total')).all()

    # Crear un diccionario de homicidios por entidad
    homicidios_dict = {item['entidad__nombre']: item['total_homicidios'] for item in homicidios_data}

    # Lista de entidades (estados) y coordenadas de los estados
    coordenadas_estados = {
        "Aguascalientes": (21.8833, -102.2916),
        "Baja California": (32.6519, -115.4683),
        "Baja California Sur": (24.1426, -110.3107),
        "Campeche": (19.8454, -90.5238),
        "Chiapas": (16.7569, -93.1292),
        "Chihuahua": (28.6321, -106.0691),
        "Ciudad de México": (19.4326, -99.1332),
        "Coahuila": (27.0587, -101.7068),
        "Colima": (19.2433, -103.7250),
        "Durango": (24.0226, -104.6576),
        "Estado de México": (19.3286, -99.6760),
        "Guanajuato": (21.0190, -101.2574),
        "Guerrero": (17.4392, -99.5451),
        "Hidalgo": (20.0911, -98.7624),
        "Jalisco": (20.6767, -103.3475),
        "Michoacán": (19.7008, -101.1844),
        "Morelos": (18.6813, -99.1013),
        "Nayarit": (21.7514, -104.8455),
        "Nuevo León": (25.6866, -100.3161),
        "Oaxaca": (17.0732, -96.7266),
        "Puebla": (19.0413, -98.2062),
        "Querétaro": (20.5888, -100.3899),
        "Quintana Roo": (19.1817, -88.4791),
        "San Luis Potosí": (22.1565, -100.9855),
        "Sinaloa": (24.8044, -107.4937),
        "Sonora": (29.0729, -110.9559),
        "Tabasco": (17.9897, -92.9475),
        "Tamaulipas": (24.2669, -98.8363),
        "Tlaxcala": (19.3190, -98.1997),
        "Veracruz": (19.1738, -96.1342),
        "Yucatán": (20.6846, -89.1860),
        "Zacatecas": (22.7709, -102.5832)
    }

    # Configurar el gráfico
    fig = go.Figure()
    escala_tamano = 0.1
    tamano_max = 50

    # Añadir los datos al gráfico
    for entidad, homicidios in homicidios_dict.items():
        lat, lon = coordenadas_estados.get(entidad, (0, 0))
        tamano = min(10 + homicidios * escala_tamano, tamano_max)

        fig.add_trace(go.Scattermapbox(
            lat=[lat],
            lon=[lon],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=tamano,
                color='red'
            ),
            text=f"{entidad}: {homicidios} homicidios",
            name=entidad
        ))

    # Configurar el layout del mapa
    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            style='open-street-map',
            bearing=0,
            center=dict(lat=23.6345, lon=-102.5528),
            pitch=0,
            zoom=5
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    # Convertir el gráfico a formato JSON
    graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)

    # Pasar el año seleccionado y el gráfico al contexto
    return render(request, 'homicidios/dashboard.html', {
        'graph_json': graph_json,
        'selected_year': year,
        'years': range(2019, 2025)  # Años de 2019 a 2024
    })


def mostrar_homicidios(request):
    homicidios = Homicidio.objects.all()
    return render(request, 'homicidios/mostrar_homicidios.html', {'homicidios': homicidios})
