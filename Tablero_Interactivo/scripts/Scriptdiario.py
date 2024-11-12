import requests
from datetime import datetime, timedelta
import os

# Definir la ruta de la carpeta de destino
carpeta_destino = "../archivos"

# Asegurarse de que la carpeta existe
os.makedirs(carpeta_destino, exist_ok=True)


# Función para descargar el PDF con '_v2'
def descargar_pdf(url, fecha):
    # Ruta completa para el archivo con '_v2'
    filename_v2 = os.path.join(carpeta_destino, f"homicidios_{fecha}_v2.pdf")

    # Verificar si ya existe el archivo '_v2'
    if os.path.exists(filename_v2):
        print(f"Ya existe: {filename_v2}")
        return

    # Intentar descargar el archivo con '_v2'
    response = requests.get(url)

    if response.status_code == 200:
        with open(filename_v2, 'wb') as file:
            file.write(response.content)
        print(f"Descargado: {filename_v2}")
    else:
        print(f"El archivo {url} no está disponible.")


# Rango de fechas
inicio = datetime(2019, 4, 3)
fin = datetime.now()  # Fecha actual como fin del rango

# Iterar sobre el rango de fechas
fecha_actual = inicio
while fecha_actual <= fin:
    # Formatear la fecha como DDMMYYYY
    fecha_str = fecha_actual.strftime('%d%m%Y')
    # Generar la URL con '_v2'
    url = f"http://informeseguridad.cns.gob.mx/files/homicidios_{fecha_str}_v2.pdf"
    # Descargar el archivo PDF
    descargar_pdf(url, fecha_str)
    # Avanzar al siguiente día
    fecha_actual += timedelta(days=1)
