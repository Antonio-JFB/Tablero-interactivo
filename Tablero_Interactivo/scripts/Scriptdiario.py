import requests
from datetime import datetime, timedelta
import os
import re

# Definir la ruta de la carpeta de destino
carpeta_destino = "../archivos"

# Asegurarse de que la carpeta existe
os.makedirs(carpeta_destino, exist_ok=True)


# Función para encontrar la fecha del último archivo descargado
def obtener_ultima_fecha():
    archivos = os.listdir(carpeta_destino)
    fechas = []

    # Extraer fechas de los archivos que sigan el patrón 'homicidios_DDMMYYYY_v2.pdf'
    for archivo in archivos:
        match = re.search(r'homicidios_(\d{8})_v2\.pdf', archivo)
        if match:
            fecha_str = match.group(1)
            fecha = datetime.strptime(fecha_str, '%d%m%Y')
            fechas.append(fecha)

    # Retornar la fecha más reciente, o una fecha inicial si no hay archivos
    return max(fechas) if fechas else datetime(2019, 4, 3)


# Función para descargar el PDF con '_v2'
def descargar_pdf(url, fecha):
    filename_v2 = os.path.join(carpeta_destino, f"homicidios_{fecha}_v2.pdf")

    if os.path.exists(filename_v2):
        print(f"Ya existe: {filename_v2}")
        return

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename_v2, 'wb') as file:
            file.write(response.content)
        print(f"Descargado: {filename_v2}")
    else:
        print(f"El archivo {url} no está disponible.")


# Obtener la fecha de inicio desde el último archivo
inicio = obtener_ultima_fecha() + timedelta(days=1)  # Día siguiente al último archivo
fin = datetime.now()  # Fecha actual como fin del rango

# Iterar sobre el rango de fechas
fecha_actual = inicio
while fecha_actual <= fin:
    fecha_str = fecha_actual.strftime('%d%m%Y')
    url = f"http://informeseguridad.cns.gob.mx/files/homicidios_{fecha_str}_v2.pdf"
    descargar_pdf(url, fecha_str)
    fecha_actual += timedelta(days=1)
