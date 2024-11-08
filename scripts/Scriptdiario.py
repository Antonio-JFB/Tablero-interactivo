import requests
from datetime import datetime, timedelta
import os
import re

# Función para descargar el PDF
def descargar_pdf(url, fecha):
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"homicidios_{fecha}.pdf"
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Descargado: {filename}")
    else:
        print(f"El archivo {url} no está disponible.")

# Función para obtener la última fecha de los archivos descargados
def obtener_ultima_fecha():
    # Busca archivos que coincidan con el patrón 'homicidios_DDMMYYYY.pdf'
    archivos = [f for f in os.listdir() if re.match(r"homicidios_\d{8}\.pdf", f)]
    fechas = []

    for archivo in archivos:
        # Extrae la fecha del nombre del archivo
        fecha_str = re.search(r"\d{8}", archivo).group()
        fecha = datetime.strptime(fecha_str, "%d%m%Y")
        fechas.append(fecha)

    # Si hay archivos, devuelve la última fecha; si no, devuelve una fecha inicial
    return max(fechas) if fechas else datetime(2019, 1, 1)

# Fecha de inicio y fin
fecha_inicio = obtener_ultima_fecha() + timedelta(days=1)
fecha_fin = datetime.now()

# Iterar desde la última fecha registrada hasta hoy
fecha_actual = fecha_inicio
while fecha_actual <= fecha_fin:
    # Formatear la fecha como DDMMYYYY
    fecha_str = fecha_actual.strftime('%d%m%Y')

    # Generar la URL
    url = f"http://informeseguridad.cns.gob.mx/files/homicidios_{fecha_str}.pdf"

    # Descargar el archivo PDF
    descargar_pdf(url, fecha_str)

    # Avanzar al siguiente día
    fecha_actual += timedelta(days=1)
